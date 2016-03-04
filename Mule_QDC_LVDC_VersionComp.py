# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:54:11 2016

@author: droy2
"""
import filecmp
import difflib
import shutil
import subprocess
import shlex
import getpass
import smtplib
#QDCPOD3_Servers =["pprdempa3300.corp.intuit.net","pprdempa3301.corp.intuit.net"]
QDCPOD3_Servers =["xxx.xxx.xxx.xxx,yyy.yyy.yyy.yy"] # Server Names are commented for Safety/Security
QDCPOD4_Servers =["xxx.xxx.xxx.xxx,yyy.yyy.yyy.yy"]
LVDCPod4_Servers=["xxx.xxx.xxx.xxx,yyy.yyy.yyy.yy"]
LVDCPod3_Servers=["xxx.xxx.xxx.xxx,yyy.yyy.yyy.yy"]
Pod_List= ["QDCPOD3_Servers","QDCPOD4_Servers"]
Pod3QDCvsPod3LVDC =["xxx.xxx.xxx.xxx,yyy.yyy.yyy.yy"]
Pod4QDCvsPod4LVDC =["xxx.xxx.xxx.xxx,yyy.yyy.yyy.yy"]

QDC_Servers_Tomcat=[["xxx.xxx.xxx.xxx,yyy.yyy.yyy.yy"]
#qdcfilesp3=['pod3qdc.txt','pod3qdc1.txt','pod3qdc2.txt','pod3qdc3.txt']

G_SANITY_FLAG_QDC_POD3='Y'

def main():
    
    
    print('Start of the Program ################START#######################################')
    print('Now Sanity Checking if All Versions  across Pod 3 QDC are same \n')
    print ('##################################################################################\n')
    sanityCheckPod(QDCPOD3_Servers,"mule")
    print ('##################################################################################\n')
    print('Now Sanity Checking if All Versions across Pod 4 QDC are same\n')
    sanityCheckPod(QDCPOD4_Servers,"mule")
    print ('##################################################################################\n')
    print('Now Sanity Checking if All Versions  across Pod 3 LVDC are same\n')
    sanityCheckPod(LVDCPod3_Servers,"mule")
    print ('##################################################################################\n')
    print('Now Sanity Checking if All Versions  across Pod 4 LVDC are same\n')
    sanityCheckPod(LVDCPod4_Servers,"mule")
    print ('##################################################################################\n')
    
    print ('############ Now Doing Sanity Checks across Pods ####################')
    print('Now Sanity Checking if All Versions  across Pod 3 QDC and Pod 3 LVDC same\n')
    sanityCheckPod(Pod3QDCvsPod3LVDC,"mule")
    print ('##################################################################################\n')
    print('Now Sanity Checking if All Versions  across Pod 4 QDC and Pod 4 LVDC same\n')
    sanityCheckPod(Pod4QDCvsPod4LVDC,"mule")
    print ('##################################################################################\n')
    print('Now Sanity Checking if All properties file Across QDC Pod 3 DC are same\n')
    sanityCheckProperties(QDCPOD3_Servers,"qydc","mule")
    print ('##################################################################################\n')
    print('Now Sanity Checking if All properties file Across QDC Pod 4 DC are same\n')
    sanityCheckProperties(QDCPOD4_Servers,"qydc","mule")
    print ('##################################################################################\n')
    print('Now Sanity Checking if All properties file Across LVDC Pod 3 DC are same\n')
    sanityCheckProperties(LVDCPod3_Servers,"lvdc","mule")
    print ('##################################################################################\n')
    print('Now Sanity Checking if All properties file Across LVDC Pod 4 DC are same\n')
    sanityCheckProperties(LVDCPod4_Servers,"lvdc","mule")
    print('End of the Program ################END#######################################')
    
    print('Now Sanity Checking for Tomcat App Versions \n')
    
    print('Now Sanity Checking if All Versions  across  QDC Tomcat are same \n')
    print ('##################################################################################\n')
    sanityCheckPod(QDC_Servers_Tomcat,"tomcat")
    print ('##################################################################################\n')
    print('Now Sanity Checking if All Versions across LVDC Tomcat are same\n')
    sanityCheckPod(LVDC_Servers_Tomcat,"tomcat")
    
    print('Now Sanity Checking for Tomcat Properties Files \n')
    
    print('Now Sanity All Tomcat Properties across QDC \n')
    
    sanityCheckProperties(QDC_Servers_Tomcat,"NOTREQUIRED","tomcat")
    
    print('Now Sanity All Tomcat Properties across LVDC \n')
    
    sanityCheckProperties(LVDC_Servers_Tomcat,"NOTREQUIRED","tomcat")
    
    
    print ('##################################END################################################\n')
    
    
    

def sanityCheckPod(myList = [], *args):
    
    
    #print('Will do a sanity check on Pod  and check if all versions are same across the Pod hosts \n')
    QDCPOD4_Servers=myList
    for pod3qdc in QDCPOD4_Servers:
        
        #print('Creating the files for Pod4 QDC')
        server=pod3qdc
        if args[0]== "mule":
            
            subprocess.call(shlex.split('ssh applmgr@%s  for n in /mule/mule-ee/apps/*; do echo "$n"; done > /tmp/%s.txt' %(server,pod3qdc)))
            #print('Getting the Files to local')        
            subprocess.call(shlex.split('scp applmgr@%s:/tmp/%s.txt ./' %(server,pod3qdc)))
       
       
        else :
            subprocess.call(shlex.split('ssh deploy@%s  sh /home/deploy/version.sh > /tmp/%s.txt' %(server,pod3qdc)))
            
            subprocess.call(shlex.split('scp deploy@%s:/tmp/%s.txt ./' %(server,pod3qdc)))
            
    
    
    #print('Comparing the Pod vs all other Hosts in the Pod')
    
    for cmp in QDCPOD4_Servers:
        
    
        if filecmp.cmp(QDCPOD4_Servers[0]+'.txt',cmp+'.txt'):
           
           print('All versions between ' + QDCPOD4_Servers[0] +'     and  '+ cmp +' are same')
            
        else:
            
            print('There are diffrences in version between the files indicated by (+) and  (-)  sign\n')
            print('The (+) or (-) sign indicates that the respective App/File is missing/additional in the second Server in comparision  sign\n')
            print('#########The diffrences between ' +QDCPOD4_Servers[0] + '  and   ' + cmp +'  are############# \n')
            diff = difflib.ndiff(open(QDCPOD4_Servers[0]+'.txt').readlines(),open(cmp+'.txt').readlines())
            delta = ''.join(diff)
            print (delta)
            global G_SANITY_FLAG_QDC_POD3
            G_SANITY_FLAG_QDC_POD3='N'

        

def sanityCheckProperties(myList = [], *args):
    
    PODServers=myList
    for podservers in PODServers:
        
        server=podservers
        
        if args[1]=="mule" :
        
        
            
            subprocess.call(shlex.split('ssh applmgr@%s  cat /mule/mule-ee/conf/webs-mule-global-prd.properties /mule/mule-ee/conf/webs-mule-%s-prd.properties /mule/mule-ee/conf/webs-mule-prd-password.properties>/tmp/%s.properties' %(server,args[0],podservers)))
            subprocess.call(shlex.split('scp applmgr@%s:/tmp/%s.properties ./' %(server,podservers)))
            
        else :
            
            
            subprocess.call(shlex.split('ssh deploy@%s  cat /app/tomcat/conf/global-application-prd.properties /app/tomcat/conf/global-passwords-prd.properties > /tmp/%s.properties' %(server,podservers)))
            subprocess.call(shlex.split('scp deploy@%s:/tmp/%s.properties ./' %(server,podservers)))
            
    
    for cmp in PODServers:
        
    
        if filecmp.cmp(PODServers[0]+'.properties',cmp+'.properties'):
           
           print('All versions between ' + PODServers[0] +'     and  '+ cmp +' are same')
            
        else:
            
            print('There are diffrences in version between the files indicated by (+) and  (-)  sign\n')
            print('The (+) or (-) sign indicates that the respective App/File is missing/additional in the second Server in comparision  sign\n')
            print('#########The diffrences between ' +PODServers[0] + '  and   ' + cmp +'  are############# \n')
            diff = difflib.ndiff(open(PODServers[0]+'.properties').readlines(),open(cmp+'.properties').readlines())
            delta = ''.join(diff)
            print (delta)
            global G_SANITY_FLAG_QDC_POD3
            G_SANITY_FLAG_QDC_POD3='N'


    
if __name__ == "__main__": main()
    
    
    
    
    