Feature: DHCPv6 Release
    Those are tests for DHCPv6 release process.
    
@v6 @dhcp6 @status_code @release
    Scenario: v6.statuscode.nobinding-release-noleases
	## Testing server ability server ability perform RELEASE - REPLY message exchange.
	## Try to release non-existing leases.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA_NA with suboption status-code with code NoBinding
	##					Status code with code NoBinding.
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 3.
	Response MUST include option 13.
	Response option 13 MUST contain statuscode 3.

	References: RFC3315 section 18.2.6.	

@v6 @dhcp6 @status_code @release
    Scenario: v6.statuscode.nobinding-release
	## Testing server ability server ability perform RELEASE - REPLY message exchange.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	##						Generate new IA
	## 						RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA_NA with suboption status-code with code NoBinding
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Generate new IA.
	Client adds saved options. And Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 3.
	
	References: RFC3315 section 18.2.6.
	
@v6 @dhcp6 @status_code @release
    Scenario: v6.statuscode.nobinding-release-new-client-id
	## Testing server ability server ability perform RELEASE - REPLY message exchange.
	## Try to release existing leases but using different client ID.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	##						Generate new Client id
	## 						RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA_NA with suboption status-code with code NoBinding
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Generate new Client_ID.
	Client adds saved options. And Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 3.
	
	References: RFC3315 section 18.2.6.	

@v6 @dhcp6 @status_code @release
    Scenario: v6.statuscode.nobinding-release-advertise
	## Testing server ability server ability perform RELEASE - REPLY message exchange.
	## That's 'double check' after v6.statuscode.nobinding-release test,
	## to make sure that lease weren't released.
	##
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	##						Generate new IA
	## 						RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE	
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA_NA with suboption status-code with code NoAddrAvail
	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::1 pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client saves server-id option from received message.
	Client adds saved options. And DONT Erase.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Generate new IA.
	Client adds saved options. And Erase.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 2.
	
	References: RFC3315 section 18.2.6.
		
@v6 @dhcp6 @status_code @release
    Scenario: v6.statuscode.nobinding-release-restart
	## Testing server ability server ability perform RELEASE - REPLY message exchange.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	##				Clear leases by restarting server
	## 						RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					IA_NA with suboption status-code with code NoBinding	
	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.

	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.

	Test Procedure:	
	Restart DHCP server.
	Client requests option 7.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 13. 
	Response sub-option 13 from option 3 MUST contain statuscode 3.
	
	References: RFC3315 section 18.2.6.
	
@v6 @dhcp6 @status_code @release
    Scenario: v6.statuscode.success-release
	## Testing server ability server ability perform RELEASE - REPLY message exchange.
	## Message details 		Client		Server
	## 						SOLICIT -->
	## 		   						<--	ADVERTISE
	## 						REQUEST -->
	## 		   						<--	REPLY
	##				Clear leases by restarting server
	## 						RELEASE -->
	##					  		    <--	REPLY
	## Pass Criteria:
	## 				REPLY MUST include option:
	##					client-id
	##					server-id
	##					status-code with code Success

	Test Setup:
	Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
	DHCP server is started.

	Test Procedure:
	Client requests option 7.
	Client sends SOLICIT message.

	Pass Criteria:
	Server MUST respond with ADVERTISE message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	Response option 3 MUST contain sub-option 5.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends REQUEST message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 3.
	
	Test Procedure:
	Client copies IA_NA option from received message.
	Client copies server-id option from received message.
	Client sends RELEASE message.
	
	Pass Criteria:
	Server MUST respond with REPLY message.
	Response MUST include option 1.
	Response MUST include option 2.
	Response MUST include option 13. 
	Response option 13 MUST contain statuscode 0.
		
	References: RFC3315 section 18.2.6.
	