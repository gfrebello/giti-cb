from pki import *
from server_org1 import *
import subprocess
import os

FILE_PATH = "data.enc"

def environment_variables ():
    try:

        pwd = subprocess.Popen("pwd", shell=True, stdout=subprocess.PIPE).stdout
        pwd_string = str(pwd.read().decode())
        pwd_string = pwd_string.rstrip()
        new_path_string = pwd_string + "/../bin"
        fabric_cfg_path = pwd_string + "/../config/"
        rootcert_file_path = pwd_string + "/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt"
        mspconfigpath = pwd_string + "/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp"

        os.environ["PATH"] += os.pathsep + new_path_string
        os.environ["FABRIC_CFG_PATH"] = fabric_cfg_path
        os.environ["CORE_PEER_TLS_ENABLED"] = "true"
        os.environ["CORE_PEER_LOCALMSPID"] = "\"Org1MSP\""
        os.environ["CORE_PEER_TLS_ROOTCERT_FILE"] = rootcert_file_path
        os.environ["CORE_PEER_MSPCONFIGPATH"] = mspconfigpath
        os.environ["CORE_PEER_ADDRESS"] = "localhost:7051"
    except:
        raise Exception("Failed to set environment variables")
    
def issue_request (data_keys, dst_org, uid):
    command = "peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile \"${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem\" -C mychannel -n global-bc --peerAddresses localhost:7051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt\" --peerAddresses localhost:9051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt\" -c \'{\"function\":\"IssueRequest\",\"Args\":[\""+ data_keys + "\",\"" + uid + "\",\"usig\",\"upubkey\",\""+dst_org+"\",\"Org2\"]}\'"
    print("Issuing command: " + command)
    command_result = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE).stdout
    print(str(command_result.read().decode()))

def issue_response (req_id, result, error_reason, entry_point):
    command = "peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile \"${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem\" -C global-channel -n global-bc --peerAddresses localhost:7051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt\" --peerAddresses localhost:9051 --tlsRootCertFiles \"${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt\" -c \'{\"function\":\"IssueRequest\",\"Args\":[\""+ req_id + "\",\"" + result + "\",\"" + error_reason + "\",\""+ entry_point + "\"]}\'"
    print("Issuing command: " + command)
    command_result = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE).stdout
    print(str(command_result.read().decode()))



def main():
    message = server()
    message_info = message.decode("utf-8").split("|")
    environment_variables()
    issue_request(message_info[0], message_info[1])

if __name__ == "__main__":
    main()
