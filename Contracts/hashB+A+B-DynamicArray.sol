// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract Egg_Random_Framwork {
    
    struct Order {
        bytes32 hashB; 
        uint256 A; 
        uint256 B; 
        uint256 R;
    }

    // Order[] memory Orders;
    mapping (uint256 => Order) public Orders;

    uint256 head;
    uint256 mid;
    uint256 tail;
    bool public paused = false;
    address private boss;
    address private admin;

    constructor () {
        boss = msg.sender;
        admin = msg.sender;
    }


    modifier onlyBoss {
        require(msg.sender == boss);
        _;
    }


    modifier onlyAdmin {
        require(msg.sender == admin);
        _;
    }    


    function TrueRandom(uint256 _A, uint256 _B) private pure returns (uint256) {
        return uint256(keccak256(abi.encodePacked(_A, _B)));
    }


    function RANDOM(uint256 _A) public pure returns (bytes32) {
        return keccak256(abi.encodePacked(_A));
    }


    function Prepare(bytes32 _hashB) external onlyAdmin {
        Orders[head].hashB = _hashB;
        head++;
    }    


    function Request(uint256 _a) public returns (uint256) {
        require(mid < head, "Overflow Protection: There is no unprocessed order exist");
        require(!paused, "Activity is paused");
        Orders[mid].A = _a;
        mid++;

        return mid;
    }


    function verify(uint256 _b) external onlyAdmin {
        require(keccak256(abi.encode(_b)) == Orders[tail].hashB, "hash is not correct");
        Orders[tail].B = _b;
        Orders[tail].R = TrueRandom(Orders[tail].A, Orders[tail].B);
        tail++;
    }    


    function pause(bool _state) public onlyAdmin {
        paused = _state;
    }


    function setAdmin(address _admin) public onlyBoss {
        admin = _admin;
    }

/*

    function pay_me_and_say_sth(string memory _say_sth) public payable {
        require(msg.value >= HighestPrice + gap, 'Incorrect value sent');

        payable(admin).transfer(msg.value);
        something = _say_sth;
        HighestPrice = msg.value;

        emit aPayment(msg.sender, msg.value, _say_sth);
    }

    function what_do_you_say() external view returns (string memory) {
        return something;
    }

    function now_price() external view returns (uint256) {
        return HighestPrice;
    }

    function now_gap() external view returns (uint256) {
        return gap;
    }

    function setPrice(uint256 _price) external onlyAdmin {
        HighestPrice = _price;
    }

    function setGap(uint256 _gap) external onlyAdmin {
        gap = _gap;
    }
*/

}