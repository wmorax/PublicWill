import os, requests, json, threading

ak='d4abe543-bbd9-446c-8d83-088fea42a720'
secret='pLIh1bM2fAaJYwI733JUmble270='
region="api2"

def token():
    url="https://{}.prismacloud.io/login".format(region)
    payload=json.dumps({"password":secret,'username':ak})
    headers={
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8'
    }
    response=requests.request('POST',url,headers=headers,data=payload)
    response=json.loads(response.content)
    return response['token']

def policy_list():
    url="https://{}.prismacloud.io/policy".format(region)
    payload={'policy.enabled':False}
    headers={
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token()
    }
    response=requests.request('GET',url,headers=headers,json=payload)
    print(response)
    response=json.loads(response.content)
    return response

def build_policy_filter():

    allPolicies=policy_list()
    allBuildPolicies=[]

    for x in allPolicies:
        for y in x['policySubTypes']:
            if y.lower()=='build' and x['enabled']==False:
                row={
                    "policyId":x['policyId'],
                    "name":x['name']
                }
                allBuildPolicies.append(row)
                del row
    return allBuildPolicies

def policy_patcher(policyId):
    url='https://{}.prismacloud.io/policy/{}/status/true'.format(region,policyId)
    headers={
        'Content-Type': 'application/json; charset=UTF-8',
        'Accept': 'application/json; charset=UTF-8',
        'x-redlock-auth': token()
    }
    response=requests.request('PATCH',url,headers=headers)
    return response

if __name__=="__main__":
    allBuildPoliciesGlobal=build_policy_filter()
    for x in allBuildPoliciesGlobal:
        t=threading.Thread(target=policy_patcher, args=[x['policyId']])
        # policy_patcher(x['policyId'])
        try:
            t.start()
            print(x['name'],'- was successfully enabled')
        except:
            print(x['name'],'- was NOT successfully enabled')
    try:
        t.join()
    except:
        print('algo salio mal')
