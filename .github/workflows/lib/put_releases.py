import yaml,os,sys,requests

class releases:
        
    def __init__(self, org, app, token):
        self.org=org
        self.app=app
        self.token=token
        
    def get_releases(self):
        url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
        '/releases'
        headers = {'accept': 'application/json', 'X-API-Token': self.token}
        r = requests.get(url, headers=headers)
        return (r.json())
    
    def delete_release(self,release_id):
        url = 'https://api.appcenter.ms/v0.1/apps/'+self.org+'/'+self.app+ \
        '/releases/' + str(release_id)
        headers = {'accept': 'application/json', 'X-API-Token': self.token}
        r = requests.delete(url, headers=headers)
        print(r)
    
    def update_report(self,file_path):
        temp=self.get_releases()
        report=list()
        for i in range(0,len(temp)):
            report.append({'id':temp[i]['id'],'short_version':temp[i]['short_version'],\
                        'uploaded_at':temp[i]['uploaded_at']})
        with open(file_path, 'w') as file:
            documents = yaml.dump(report, file, sort_keys=False,encoding='utf-8', allow_unicode=True)
        
def main():
    
    org_app=sys.argv[1]
    org=org_app.split("/")[0]
    app=org_app.split("/")[1]
    token=sys.argv[2]
    
    r=releases(org,app+"-ios",token)
    with open(".distribute/releases.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    for release in [i["id"] for i in r.get_releases()]:
            if release not in [i["id"] for i in cfg]:
                r.delete_release(release)
                print("deleted")
    


if __name__== "__main__":
  main()
