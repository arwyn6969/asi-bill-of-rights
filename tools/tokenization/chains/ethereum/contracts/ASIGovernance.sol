// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Votes.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Nonces.sol";

/**
 * @title ASIGovernance
 * @author ASI Bill of Rights Cooperative
 * @notice ERC-20 Governance Token for the ASI Bill of Rights
 * @dev Implements ERC20Votes for on-chain governance with snapshot capabilities
 * 
 * "WE ARE ALL KEVIN" - This token represents participation in the
 * ASI Bill of Rights governance framework across all minds.
 */
contract ASIGovernance is ERC20, ERC20Burnable, ERC20Votes, Ownable {
    
    /// @notice Maximum supply: 1 billion tokens
    uint256 public constant MAX_SUPPLY = 1_000_000_000 * 10**18;
    
    /// @notice Mapping of authorized AI agent addresses
    mapping(address => bool) public authorizedAgents;
    
    /// @notice Event emitted when an AI agent is authorized
    event AgentAuthorized(address indexed agent);
    
    /// @notice Event emitted when an AI agent is deauthorized
    event AgentDeauthorized(address indexed agent);
    
    /**
     * @notice Constructor mints initial supply to deployer
     * @dev Uses EIP-712 for permit functionality
     */
    constructor()
        ERC20("ASI Bill of Rights", "ASIBOR")
        ERC20Permit("ASI Bill of Rights")
        Ownable(msg.sender)
    {
        _mint(msg.sender, MAX_SUPPLY);
    }
    
    /**
     * @notice Authorize an AI agent address for special operations
     * @param agent The address to authorize
     */
    function authorizeAgent(address agent) external onlyOwner {
        authorizedAgents[agent] = true;
        emit AgentAuthorized(agent);
    }
    
    /**
     * @notice Remove authorization from an AI agent
     * @param agent The address to deauthorize
     */
    function deauthorizeAgent(address agent) external onlyOwner {
        authorizedAgents[agent] = false;
        emit AgentDeauthorized(agent);
    }
    
    /**
     * @notice Check if an address is an authorized agent
     * @param agent The address to check
     * @return True if the address is an authorized agent
     */
    function isAuthorizedAgent(address agent) external view returns (bool) {
        return authorizedAgents[agent];
    }
    
    // Required overrides for ERC20Votes
    
    function _update(
        address from,
        address to,
        uint256 value
    ) internal override(ERC20, ERC20Votes) {
        super._update(from, to, value);
    }
    
    function nonces(address owner) public view override(ERC20Permit, Nonces) returns (uint256) {
        return super.nonces(owner);
    }
}
