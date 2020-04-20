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
     
    def update_report(self):
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
        return report
        #with open(file_path, 'w',encoding="utf-8") as file:
        #    documents = yaml.dump(report, file, sort_keys=False,allow_unicode=True, default_flow_style=False)
        
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

  
def merge(file1,file2):
  report=list()
  group=dict()
  members=dict()

  for i in range(0,len(file1)):
    group["name"]=file1[i]["name"]
    group["is_public"]=file1[i]["is_public"]
    members["android"]=file1[i]["members"]
    members["ios"]=file2[i]["members"]
    group["members"]=members
    group["releases"]=file1[i]["releases"]
    report.append(group)
    group=dict()
    members=dict()

  file_path=".distribute/groups.yml"
  with open(file_path, 'w',encoding="utf-8") as file:
            documents = yaml.dump(report, file, sort_keys=False,allow_unicode=True, default_flow_style=False)

def main():
    
    org_app=sys.argv[1]
    
    org=org_app.split("/")[0]
    app=org_app.split("/")[1]
    token=sys.argv[2]
    
    g1=groups(org,app+"-ios",token)
    g2=groups(org,app+"-android",token)
    

    #file1=yaml.dump(g1.update_report(), sort_keys=False,allow_unicode=True, default_flow_style=False)
    #file2=yaml.dump(g2.update_report(), sort_keys=False,allow_unicode=True, default_flow_style=False)

    merge(g1.update_report(),g2.update_report()) 


if __name__== "__main__":
  main()
