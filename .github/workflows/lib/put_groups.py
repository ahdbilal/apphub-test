import yaml,os,sys,requests,csv

class groups:
    
    def __init__(self, org, app, token):
      self.org=org
      self.app=app
      self.token=token

    def get_groups(self):
      url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
      '/distribution_groups'
      headers = {'accept': 'application/json', 'X-API-Token': self.token}
      r = requests.get(url, headers=headers)
      return (r.json())

    def add_group(self,name,is_public):
      url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
      '/distribution_groups'
      headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'X-API-Token': self.token}
      payload = '\"name\": \"{0}\",\"display_name\": \"{0}\" , \"is_public\": {1}'.format(name,is_public)
      payload = '{' + payload + '}'
      r = requests.post(url, data=payload,headers=headers)
      print(r)

    def delete_group(self,name):
      url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
      '/distribution_groups/' + name
      headers = {'accept': 'application/json', 'X-API-Token': self.token}
      r = requests.delete(url, headers=headers)
      print(r)

    def get_users(self, name):
      url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
      '/distribution_groups/' + name + '/members'
      headers = {'accept': 'application/json', 'X-API-Token': self.token}
      r = requests.get(url, headers=headers)
      return (r.json())

    def add_user(self,name,email):
      url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
      '/distribution_groups/' + name + '/members'
      headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'X-API-Token': self.token}
      payload = '\"user_emails\": [\"{0}\"]'.format(email)
      payload = '{' + payload + '}'
      r = requests.post(url, data=payload,headers=headers)
      print(r)

    def delete_user(self,name,email):
      url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
      '/distribution_groups/' + name + '/members/bulk_delete'
      headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'X-API-Token': self.token}
      payload = '\"user_emails\": [\"{0}\"]'.format(email)
      payload = '{' + payload + '}'
      r = requests.post(url, data=payload,headers=headers)
      print(r)
        
    def get_releases(self,name):
        url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
        '/distribution_groups/' + name + '/releases'
        headers = {'accept': 'application/json', 'X-API-Token': self.token}
        r = requests.get(url, headers=headers)
        return (r.json())

    def add_release(self,group_id,release_id):
        url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
        '/releases/' + release_id + '/groups'
        headers = {'accept': 'application/json', 'Content-Type': 'application/json', 'X-API-Token': self.token}
        payload = '\"id\": \"{0}\", \"mandatory_update\": false, \"notify_testers\": true'.format(group_id)
        payload = '{' + payload + '}'
        r = requests.post(url, data=payload,headers=headers)
        print(r)

    def delete_release(self,group_id,release_id):
        url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
        '/releases/' + release_id + '/groups/'+group_id
        headers = {'accept': 'application/json', 'X-API-Token': self.token}
        r = requests.delete(url ,headers=headers)
        print(r)
     
    def update_report(self,file_path):
        temp=self.get_groups()
        report=list()
        mark=False
        for i in range(0,len(temp)):
            users=[i['email'] for i in self.get_users(temp[i]['name'])]
            for file in os.listdir(".distribute/alias/"):
                if file.endswith(".csv"):
                    if set(users)==set(manage_alias(os.path.join(".distribute/alias/", file))):
                        report.append({'name':temp[i]['name'],'is_public':temp[i]['is_public'],
                                      'members':["include: "+file],
                                      'releases':[i['id'] for i in self.get_releases(temp[i]['name'])]})
                        mark=True
                  
                
            if mark==False:
                report.append({'name':temp[i]['name'],'is_public':temp[i]['is_public'],
                              'members':[i['email'] for i in self.get_users(temp[i]['name'])],
                              'releases':[i['id'] for i in self.get_releases(temp[i]['name'])]})
            mark=False
        with open(file_path, 'w',encoding="utf-8") as file:
            documents = yaml.dump(report, file, sort_keys=False,encoding='utf-8', allow_unicode=True)

def manage_alias(file):
    # Open our data file in read-mode.
    csvfile = open(file, 'r',encoding='utf-8-sig')

    # Save a CSV Reader object.
    datareader = csv.reader(csvfile, delimiter=',', quotechar='"')

    # Empty array for data headings, which we will fill with the first row from our CSV.
    data_headings = []

    # Loop through each row...
    for row_index, row in enumerate(datareader):
        data_headings.append(row[0])
    
    return data_headings

def sync_groups(g,cfg,platform):

    # add group
    if cfg != None:
        for group in cfg:
            print(group["name"])
            if group["name"] not in [i["name"] for i in g.get_groups()]:
                g.add_group(group["name"],str(group["is_public"]).lower())
                print("added group: {0}".format(group["name"]))
        
            #check access settings
            #if group["is_public"] != [i["is_public"] for i in cfg if i["name"] == group["name"]][0]:
                # to do

            # add users
            if [i["members"][platform] for i in cfg if i["name"] == group["name"]][0]!=None:
                for user in [i["members"][platform] for i in cfg if i["name"] == group["name"]][0]:
                    if "include" in user:
                        alias_users=manage_alias(".distribute/alias/"+user.split(" ")[1])
                        for alias_user in alias_users:
                            if alias_user not in [i["email"] for i in g.get_users(group["name"])]:
                                g.add_user(group["name"],alias_user)
                                print("updated/added alias: {0}".format(user.split(" ")[1]))    
                    elif user not in [i["email"] for i in g.get_users(group["name"])]:
                        g.add_user(group["name"],user)
                        print("added user: {0}".format(user))
        
            #delete users
            if [i["email"] for i in g.get_users(group["name"])]==[]:
                pass
            elif [i["members"][platform]for i in cfg if i["name"] == group["name"]][0]==None:
                for user in [i["email"] for i in g.get_users(group["name"])]:
                        g.delete_user(group["name"],user)
                        print("deleted user: {0}".format(user))
            else: 
                for user in [i["email"] for i in g.get_users(group["name"])]:
                    if "include" in str([i["members"][platform] for i in cfg if i["name"] == group["name"]][0]):
                        #alias_users=manage_alias(".distribute/alias/"+user.split(" ")[1])
                        for user in [i["email"] for i in g.get_users(group["name"])]:
                            if user not in alias_users:
                                g.delete_user(group["name"],user)
                                #print("updated/deleted alias: {0}".format(user.split(" ")[1]))  
                    elif user not in [i["members"][platform] for i in cfg if i["name"] == group["name"]][0]:
                        g.delete_user(group["name"],user)
                        print("deleted user: {0}".format(user))
                # add release
                if [i["releases"] for i in cfg if i["name"] == group["name"]][0]!=None:
                    for release in [i["releases"] for i in cfg if i["name"] == group["name"]][0]:
                            if release not in [i["id"] for i in g.get_releases(group["name"])]:
                                group_id=[i["id"] for i in g.get_groups() if i["name"] == group["name"]][0]                   
                                g.add_release(group_id,str(release))
                                print("added release: {0}".format(release))

            # delete release
            if [i["id"] for i in g.get_releases(group["name"])]==[]:
                pass
            elif [i["releases"] for i in cfg if i["name"] == group["name"]][0]==None:
                for release in [i["id"] for i in g.get_releases(group["name"])]:
                    group_id=[i["id"] for i in g.get_groups() if i["name"] == group["name"]][0]                   
                    g.delete_release(group_id,str(release))
                    print("deleted release: {0}".format(release))
            else:
                for release in [i["id"] for i in g.get_releases(group["name"])]:
                        if release not in [i["releases"] for i in cfg if i["name"] == group["name"]][0]:
                            group_id=[i["id"] for i in g.get_groups() if i["name"] == group["name"]][0]                   
                            g.delete_release(group_id,str(release))
                            print("deleted release: {0}".format(release))
        
        # delete group
        for group in g.get_groups():
            if group["name"] not in [i["name"] for i in cfg]:
                g.delete_group(group["name"])
                print("deleted group: {0}".format(group["name"]))

def main():
    
    org_app=sys.argv[1]

    org=org_app.split("/")[0]
    app=org_app.split("/")[1]
    token=sys.argv[2]
    
    
    g1=groups(org,app+"-ios",token)
    g2=groups(org,app+"-android",token)
    
    with open(".distribute/groups.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
        
    sync_groups(g1,cfg,"android")
    sync_groups(g2,cfg,"ios")



if __name__== "__main__":
  main()

#python .github/workflows/lib/put_groups.py ahdbilal/apphub-test e420a4da021fe8d5fcc68c98884157719262ca8a
#python .github/workflows/lib/get_groups.py ahdbilal/apphub-test e420a4da021fe8d5fcc68c98884157719262ca8a
#python .github/workflows/lib/get_releases.py ahdbilal/apphub-test e420a4da021fe8d5fcc68c98884157719262ca8a
#python .github/workflows/lib/put_releases.py ahdbilal/apphub-test e420a4da021fe8d5fcc68c98884157719262ca8a
