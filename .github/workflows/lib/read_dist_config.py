def main():
    import yaml,os,sys

    ref=sys.argv[1]
    event=sys.argv[2]
    param=sys.argv[3]

    with open(".distribute/config.yml", 'r') as ymlfile:
        cfg = yaml.safe_load(ymlfile)

    if "pull" in event:
        ref=sys.argv[4]

    for i in range(0,len(cfg)):
        if cfg[i]['branch'] in ref and str(cfg[i]['event']) in event:
            group=cfg[i]['destinations']['group']
            ios_store=cfg[i]['destinations']['store']['ios']
            android_store=cfg[i]['destinations']['store']['android']
            mandatory_update=cfg[i]['destinations']['mandatory_update']
            notify_testers=cfg[i]['destinations']['notify_testers']
            build=cfg[i]['release']['build']
            publish=cfg[i]['release']['publish']
            prerelease=cfg[i]['release']['prerelease']
            draft=cfg[i]['release']['draft']
            break
        else:
            build=""
            publish=""
            prerelease=""
            draft=""
            group=""
            ios_store=""
            android_store=""
            mandatory_update=""
            notify_testers=""
            
    if param=="build":
        return print(build)
    elif param=="publish":
        return print(publish)
    elif param=="destinations-group":
        return print(str(group))
    elif param=="destinations-ios-store":
        return print(str(ios_store))
    elif param=="destinations-android-store":
        return print(str(android_store))
    elif param=="mandatory_update":
        return print(mandatory_update)
    elif param=="notify_testers":
        return print(notify_testers)
    elif param=="prerelease":
        return print(prerelease)
    elif param=="draft":
        return print(draft)
    else:
        return print(-1)
  
if __name__== "__main__":
  main()

#group=$(echo python3 .github/workflows/lib/read_dist_config.py "master"  "/ref/master" "destinations-group")