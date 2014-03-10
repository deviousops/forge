

Feature: DHCPv4 address request process
    Those are simple DHCPv4 tests for address assignment. During INIT-REBOOT state.

@v4 @request
    Scenario: v4.request.initreboot.success-chaddr

    Test Setup:
    Server is configured with 192.168.50.0/24 subnet with 192.168.50.1-192.168.50.1 pool.
    Server is started.

    Test Procedure:
    Client adds to message requested_addr with value 192.168.50.1.
    #With value 192.168.50.1 client  does include requested_addr.
    Client requests option 1.
    Client sends DISCOVER message.

    Pass Criteria:
    Server MUST respond with OFFER message.
    Response MUST include option 1.
    Response MUST contain yiaddr 192.168.50.1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client copies server_id option from received message.
    
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.

    Test Procedure:
    Client adds to the message requested_addr with value 192.168.50.1.
    Client requests option 1.
    Client sends REQUEST message.

    Pass Criteria:
    Server MUST respond with ACK message.
    Response MUST contain yiaddr 192.168.50.1.
	Response MUST include option 1.
    Response option 1 MUST contain value 255.255.255.0.