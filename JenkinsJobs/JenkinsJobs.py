import requests, json
from datetime import datetime
from time import time

query_string = {'tree': 'jobs[name]'
                }
url = ('jenkins url')

job_names = requests.get(url, params=query_string)  # , headers=headers)

file_name = str("JenkinsTestRunsLastSixMonths"+str(datetime.utcnow().strftime('%Y-%m-%d %H%M%S'))+".csv")

file = open(file_name, "w+")

file.write("Job name," + "Duration (seconds)," + "Time of execution," + "Result" + "\n")
print ("Creating file: " + file_name)
for job in job_names.json()["jobs"]:
    if "test" in job["name"].lower():
        job_details = (url[:len(url) - 8] + "job/" + job["name"] + "/api/json?tree=builds[fullDisplayName,result,duration,timestamp,builtOn]")
        job_details = requests.get(job_details, params=query_string)

        for job_info in job_details.json()["builds"]:
            if "SUCCESS" in job_info["result"] and (job_info["timestamp"]/1000) > (int(time()) - 15552000):
                file.write(str(job["name"]) + "," + str(round(job_info["duration"]/1000)) + "," +
                      str(datetime.utcfromtimestamp(job_info["timestamp"] / 1000).strftime('%Y-%m-%dT%H:%M:%SZ')) + "," +
                      str(job_info["result"]) + "\n")

file.close()
print ("File " + file_name + " created")