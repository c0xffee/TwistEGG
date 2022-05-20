// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract TwistEGG_Random_Framwork_v1_5 {
    

    //// Varable Declare ////
    struct order {
        bytes32 hashB; 
        uint256 A; 
        uint256 B; 
        uint256 R;
    }

    // Order[] memory Orders;
    mapping (uint256 => order) public Orders;

    // FIXed : index set to public
    uint256 public  head;
    uint256 public  mid;
    uint256 public  tail;
    bool    public  paused = false;
    address private boss;
    address private admin;


    //// Events ////
    event isPaused (bool paused);

    event Receipt  (uint256 Order_ID, 
                    address EGG_Twister, 
                    bytes32 EGG_Provider_Chosen_Number_Hash, 
                    uint256 EGG_Twister_Chosen_Number);

    event Order    (uint256 Order_ID, 
                    bytes32 EGG_Provider_Chosen_Number_Hash, 
                    uint256 EGG_Twister_Chosen_Number, 
                    uint256 EGG_Provider_Chosen_Number, 
                    uint256 True_Random_Number);


    constructor () {
        boss  = msg.sender;
        admin = msg.sender;
    }


    //// Modifier ////
    modifier onlyBoss {
        require(msg.sender == boss);
        _;
    }


    modifier onlyAdmin {
        require(msg.sender == admin);
        _;
    }    


    //// Random Functions ////
    function TrueRandom(uint256 _A, uint256 _B) private pure returns (uint256) {
        return uint256(keccak256(abi.encodePacked(_A, _B)));
    }


    function RANDOM(uint256 _A) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(_A));
    }


    //// Twist EGG Process ////
    function Prepare(bytes32 _hashB) external onlyAdmin {
        Orders[head].hashB = _hashB;
        head++;
    }    

    // FIXed : add recipt event !
    function Request(uint256 _a) public returns (uint256) {
        require(mid < head, "Overflow Protection: There is no unprocessed order exist");
        require(!paused, "Activity is paused");
        Orders[mid].A = _a;
        
        emit Receipt(mid, 
                     msg.sender, 
                     Orders[mid].hashB, 
                     Orders[mid].A);

        mid++;
        return mid-1;
    }


    function Verify(uint256 _b) external onlyAdmin {
        require(keccak256(abi.encode(_b)) == Orders[tail].hashB, "hash is not correct");
        Orders[tail].B = _b;
        Orders[tail].R = TrueRandom(Orders[tail].A, Orders[tail].B);

        emit Order(tail, 
                   Orders[tail].hashB, 
                   Orders[tail].A, 
                   Orders[tail].B, 
                   Orders[tail].R);

        tail++;
    }    


    //// Admin and Boss Only Functions ////
    function setPause(bool _state) public onlyAdmin {
        paused = _state;
        emit isPaused(paused);
    }


    function setAdmin(address _admin) public onlyBoss {
        admin = _admin;
    }

}