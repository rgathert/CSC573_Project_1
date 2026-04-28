# CSC573_Project_1
Peer to Peer System With Centralized server.

Note:
Requires python 3.x to run

Usage for the project:
Open up the main project root directory
Running the server:
Type in python src/server.py Note: This sever listens on port 7734

Running the peer:
python src/peer.py <peer_IP> peer1_rfc <server_IP> 
(server and peer IP is localhost if testing locally, IP of device if testing remotely)

Running secondary peer:
python src/peer.py <peer_IP> peer2_rfc <server_IP> 
(server and peer IP is localhost if testing locally, IP of device if testing remotely)

Commands for peer 
lookup <rfc_num>: Finds peers with that RFC number
list: Lists all within the server index
add <rfc_num> add a locally available rfc to the index
get <rfc_num> <peer_host> <peer_port> downloads an RFC from another peer
quit - Exits the command window
