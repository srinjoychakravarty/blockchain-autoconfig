 #!/bin/bash         

cd ~

#downloads blockchain files
echo distro18 | sudo -S wget https://www.multichain.com/download/multichain-2.0-beta-1.tar.gz

#unzips blockchain files
tar -xvzf multichain-2.0-beta-1.tar.gz
cd multichain-2.0-beta-1

#moves all executables to linux binary path for universal path execution
sudo mv multichaind multichain-cli multichain-util /usr/local/bin
sudo multichain-util create auditchain
y | sudo multichaind auditchain -daemon

#extracts json-rpc port to set firewall rules accordingly
var="$(sudo grep rpc-port ~/.multichain/auditchain/params.dat)"
port="$(cut -d " " -f 3 <<< $var)"
sudo ufw enable
sudo ufw allow $port

#generates 1 blockchain account for each quickbooks trial balance account
cd ~/.multichain/auditchain/
for (( i=0; i<61; ++i)); do
  sudo multichain-cli auditchain getnewaddress
  sleep 1
done

#listaddresses in blockchain node into variable and outputs to a file 
addr="$(sudo multichain-cli auditchain listaddresses)"
cd ~/blockchain-auto-config
sudo echo "$addr"  > address_list.json

#removes ismine boolean and outputs to fresh file
#awk 'NR % 4 != 0' file > file1

#extacted only address lines and output to fresh file
#awk 'NR == 1 || NR % 3 == 0' file1 > file2

#removes square bracket from first line

#activate virtualenv
source venvs/maio/bin/activate

#run python file below
sudo python parse_addresses.py
