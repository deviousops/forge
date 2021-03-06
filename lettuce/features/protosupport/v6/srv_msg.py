# Copyright (C) 2012-2013 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Wlodzimierz Wencel

#
# This file contains a number of common steps that are general and may be used
# By a lot of feature files.
#
from cookielib import debug
from features.logging_facility import get_common_logger
from features.terrain import set_options, set_values
from lettuce.registry import world
from scapy.layers.dhcp6 import *

# option codes for options and sub-options for dhcp v6
options6 = {"client-id": 1,
            "server-id": 2,
            "IA_NA": 3,
            "IN_TA": 4,
            "IA_address": 5,
            "preference": 7,
            "relay-msg": 9,
            "status-code": 13,
            "rapid_commit": 14,
            "vendor-class": 16,
            "vendor-specific-info": 17,
            "interface-id": 18,
            "sip-server-dns": 21,
            "sip-server-addr": 22,
            "dns-servers": 23,
            "domain-search": 24,
            "IA_PD": 25,
            "IA-Prefix": 26,
            "nis-servers": 27,
            "nisp-servers": 28,
            "nis-domain-name": 29,
            "nisp-domain-name": 30,
            "sntp-servers": 31,
            "information-refresh-time": 32,
            "remote-id": 37,
            "subscriber-id": 38,
            "fqdn": 39,
            "client-link-layer-addr": 79}

## ======================================================================
## ================ PREPARE MESSAGE OPTIONS BLOCK START =================


def client_requests_option(step, opt_type):
    """
    Add RequestOption to message.
    """
    if not hasattr(world, 'oro'):
        # There was no ORO at all, create new one
        world.oro = DHCP6OptOptReq()
        # Scapy creates ORO with 23, 24 options request. Let's get rid of them
        world.oro.reqopts = [] # don't request anything by default

    world.oro.reqopts.append(int(opt_type))


def client_send_msg(step, msgname, iface, addr):
    """
    Sends specified message with defined options.
    Parameters:
    msg ('<msg> message'): name of the message.
    """
    # iface and addr not used for v6 for now.

    # Remove previous message waiting to be sent, just in case this is a
    # REQUEST after we received ADVERTISE. We don't want to send SOLICIT
    # the second time.
    world.climsg = []

    if msgname == "SOLICIT":
        msg = build_msg(DHCP6_Solicit())

    elif msgname == "REQUEST":
        msg = build_msg(DHCP6_Request())

    elif msgname == "CONFIRM":
        msg = build_msg(DHCP6_Confirm())

    elif msgname == "RENEW":
        msg = build_msg(DHCP6_Renew())

    elif msgname == "REBIND":
        msg = build_msg(DHCP6_Rebind())

    elif msgname == "DECLINE":
        msg = build_msg(DHCP6_Decline())

    elif msgname == "RELEASE":
        msg = build_msg(DHCP6_Release())

    elif msgname == "INFOREQUEST":
        world.cfg["add_option"]["IA_NA"] = False
        world.cfg["add_option"]["IA_TA"] = False
        msg = build_msg(DHCP6_InfoRequest())

    else:
        assert False, "Invalid message type: %s" % msgname

    assert msg, "Message preparation failed"

    if msg:
        world.climsg.append(msg)

    get_common_logger().debug("Message %s will be sent over %s interface." % (msgname, world.cfg["iface"]))


def client_sets_value(step, value_name, new_value):
    if value_name in world.cfg["values"]:
        if isinstance(world.cfg["values"][value_name], str):
            world.cfg["values"][value_name] = str(new_value)
        elif isinstance(world.cfg["values"][value_name], int):
            world.cfg["values"][value_name] = int(new_value)
        else:
            world.cfg["values"][value_name] = new_value
    else:
        assert value_name in world.cfg["values"], "Unknown value name : %s" % value_name


def unicast_addres(step,addr_type):
    """
    Turn off sending on All_DHCP_Relay_Agents_and_Servers, and use UNICAST address.
    """
    if addr_type:
        from features.init_all import SRV_IPV6_ADDR_GLOBAL
        world.cfg["address_v6"] = SRV_IPV6_ADDR_GLOBAL
    else:
        from features.init_all import SRV_IPV6_ADDR_LINK_LOCAL
        world.cfg["address_v6"] = SRV_IPV6_ADDR_LINK_LOCAL


def client_does_include(step, opt_type, value):
    """
    Include options to message. This function refers to @step in lettuce
    """
    # value variable not used in v6
    # If you want to use options of received message to include it,
    # please use 'Client copies (\S+) option from received message.' step.
    if opt_type == "client-id":
        world.cfg["add_option"]["client_id"] = False
    elif opt_type == "wrong-client-id":
        world.cfg["add_option"]["wrong_client_id"] = True
    elif opt_type == "wrong-server-id":
        world.cfg["add_option"]["wrong_server_id"] = True
    elif opt_type == "preference":
        world.cfg["add_option"]["preference"] = True
    elif opt_type == "rapid-commit":
        world.cfg["add_option"]["rapid_commit"] = True
    elif opt_type == "time":
        world.cfg["add_option"]["time"] = True
    elif opt_type == "relay-msg":
        world.cfg["add_option"]["relay_msg"] = True
    elif opt_type == "server-unicast":
        world.cfg["add_option"]["server_uni"] = True
    elif opt_type == "status-code":
        world.cfg["add_option"]["status_code"] = True
    elif opt_type == "interface-id":
        world.cfg["add_option"]["interface_id"] = True
    elif opt_type == "reconfigure":
        world.cfg["add_option"]["reconfig"] = True
    elif opt_type == "reconfigure-accept":
        world.cfg["add_option"]["reconfig_accept"] = True
    elif opt_type == "option-request":
        world.cfg["add_option"]["option_request"] = True
    elif opt_type == "IA-PD":
        world.cfg["add_option"]["IA_PD"] = True
    elif opt_type == "IA-NA":
        world.cfg["add_option"]["IA_NA"] = False
    elif opt_type == "IA_Prefix":
        world.cfg["add_option"]["IA_Prefix"] = True
    elif opt_type == "IA_Address":
        world.cfg["add_option"]["IA_Address"] = True
    elif opt_type == "vendor-class":
        world.cfg["add_option"]["vendor_class"] = True
    elif opt_type == "vendor-specific-info":
        world.cfg["add_option"]["vendor_specific_info"] = True
    elif opt_type == "fqdn":
        world.cfg["add_option"]["fqdn"] = True
    elif opt_type == "client-link-layer-addr":
        world.cfg["add_option"]["client-link-layer-addr"] = True
    elif opt_type == "remote-id":
        world.cfg["add_option"]["remote-id"] = True
    elif opt_type == "subscriber-id":
        world.cfg["add_option"]["subscriber-id"] = True
    else:
        assert "unsupported option: " + opt_type


def add_vendor_suboption(step, code, data):
    # if code == 1 we need check if we added code = 1 before
    # if we do, we need append only data not whole suboption
    if code == 1 and len(world.vendor) > 0:
        for each in world.vendor:
            if each[0] == 1:
                each[1].append(int(data))

    # if world.vendor is empty and code == 1 add
    # code =1 and data as int (required to further conversion)
    elif code == 1:
        world.vendor.append([code, [int(data)]])

    # every other option just add
    else:
        world.vendor.append([code, str(data)])


def generate_new (step, opt):
    """
    Generate new client id with random MAC address.
    """
    if opt == 'client':
        from features.terrain import client_id, ia_id
        client_id(RandMAC())
        ia_id()
    elif opt == 'Client_ID':
        from features.terrain import client_id
        client_id(RandMAC())
    elif opt == 'IA':
        from features.terrain import ia_id
        ia_id()
    elif opt == 'IA_PD':
        from features.terrain import ia_pd
        ia_pd()

    else:
        assert False,  opt + " generation unsupported"

## ================ PREPARE MESSAGE OPTIONS BLOCK END ===================

## ============================================================
## ================ BUILD MESSAGE BLOCK START =================


def add_client_option(option):
    world.cliopts.append(option)


def add_option_to_msg(msg, option):
    # this is request_option option
    msg /= option
    return msg


def client_add_saved_option(step, erase, count = "all"):
    """
    Add saved option to message, and erase.
    """
    if count == "all":
        for each_key in world.savedmsg.keys():
            for every_opt in world.savedmsg[each_key]:
                world.cliopts.append(every_opt)
            if erase:
                world.savedmsg = {}
    else:
        if not world.savedmsg.has_key(count):
            assert False, "There is no set no. {count} in saved opotions".format(**locals())

        for each in world.savedmsg[count]:
            world.cliopts.append(each)
        if erase:
            world.savedmsg[count] = []


def vendor_option_request_convert():
    data_tmp = ''
    for each in world.vendor:
        if each[0] == 1:
            for number in each[1]:
                data_tmp += '\00' + str(chr(number))
            each[1] = data_tmp
        else:
            each[1] = each[1].replace(':', '').decode('hex')


def convert_DUID_hwaddr(value):
    tmp = world.cfg["values"]["DUID"][value:]
    hwaddr = ':'.join(tmp[i:i+2] for i in range(0, len(tmp), 2))
    return hwaddr


def convert_DUID():
    """
    We can use two types of DUID:
        DUID_LLT link layer address + time (e.g. 00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8 )
        DUID_LL link layer address (e.g. 00:03:00:01:ff:ff:ff:ff:ff:01 )

        third DUID based on vendor is not supported (also not planned to be ever supported)

        In case of using DUID_LLT:
            00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8
            00:01 - duid type, it need to be 0001 for DUID_LLT
                  00:01 - hardware type, make it always 0001
                        52:7b:a8:f0 - converted time value
                                    08:00:27:58:f1:e8 - link layer address

        In case of using DUID_LL:
            00:03:00:01:ff:ff:ff:ff:ff:01
            00:03 - duid type, it need to be 0003 for DUID_LL
                  00:01 - hardware type, make it always 0001
                        ff:ff:ff:ff:ff:01 - link layer address

        You can use two forms for each DUID type, with ":" and without.
        For example
                00:01:00:01:52:7b:a8:f0:08:00:27:58:f1:e8
            it's same as:
                00010001527ba8f008002758f1e8
            and
                00:03:00:01:ff:ff:ff:ff:ff:01
            it's same as:
                00030001ffffffffff01

        Other configurations will cause to fail test.
    """
    world.cfg["values"]["DUID"] = world.cfg["values"]["DUID"].replace(":", "")

    if world.cfg["values"]["DUID"][:8] == "00030001":
        return DUID_LL(lladdr = convert_DUID_hwaddr(8))
    elif world.cfg["values"]["DUID"][:8] == "00010001":
        return DUID_LLT(timeval = int(world.cfg["values"]["DUID"][8:16], 16), lladdr = convert_DUID_hwaddr(16))
    else:
        assert False, "DUID value is not valid! DUID: " + world.cfg["values"]["DUID"]


def client_option(msg):
    """
    Add options (like server-id, rapid commit) to message. This function refers to building message
    """

    if world.cfg["values"]["DUID"] is not None:
        world.cfg["values"]["cli_duid"] = convert_DUID()

    #server id with mistake, if you want to add correct server id, plz use 'client copies server id...'
    if world.cfg["add_option"]["wrong_server_id"]:
        msg /= DHCP6OptServerId(duid = DUID_LLT(timeval = int(time.time()), lladdr = RandMAC()))

    #client id
    if world.cfg["add_option"]["client_id"] and not world.cfg["add_option"]["wrong_client_id"]:
        if not world.cfg["relay"]:
            msg /= DHCP6OptClientId(duid = world.cfg["values"]["cli_duid"])
    elif world.cfg["add_option"]["client_id"] and world.cfg["add_option"]["wrong_client_id"]:
        msg /= DHCP6OptClientId()  # it needs to stay blank!

    elif not world.cfg["add_option"]["client_id"]:
        #world.cfg["add_option"]["client_id"] = True
        pass

    if world.cfg["add_option"]["IA_NA"] and not world.cfg["relay"] and world.cfg["values"]["IA_Address"] == "::":
        if world.oro is not None and len(world.cliopts):
            for opt in world.cliopts:
                if opt.optcode == 3:
                    break  # if there is no IA_NA/TA in world.cliopts, break..
            else:
                msg /= DHCP6OptIA_NA(iaid = int(world.cfg["values"]["ia_id"]),
                                     T1 = world.cfg["values"]["T1"],
                                     T2 = world.cfg["values"]["T2"])  # if not, add IA_NA
        else:
            msg /= DHCP6OptIA_NA(iaid = int(world.cfg["values"]["ia_id"]),
                                 T1 = world.cfg["values"]["T1"],
                                 T2 = world.cfg["values"]["T2"])  # if not, add IA_NA

    if world.cfg["add_option"]["preference"]:
        msg /= DHCP6OptPref()

    if world.cfg["add_option"]["rapid_commit"]:
        msg /= DHCP6OptRapidCommit()

    if world.cfg["add_option"]["time"]:
        msg /= DHCP6OptElapsedTime()

    if world.cfg["add_option"]["server_uni"]:
        msg /= DHCP6OptServerUnicast()

    if world.cfg["add_option"]["status_code"]:
        msg /= DHCP6OptStatusCode()

    if world.cfg["add_option"]["interface_id"]:
        msg /= DHCP6OptIfaceId(ifaceid = world.cfg["values"]["ifaceid"])

    if world.cfg["add_option"]["reconfig"]:
        msg /= DHCP6OptReconfMsg()

    if world.cfg["add_option"]["reconfig_accept"]:
        msg /= DHCP6OptReconfAccept()

    if world.cfg["add_option"]["IA_PD"]:
        msg /= DHCP6OptIA_PD(iaid = int(world.cfg["values"]["ia_pd"]),
                             T1 = world.cfg["values"]["T1"],
                             T2 = world.cfg["values"]["T2"])

    if world.cfg["add_option"]["option_request"]:
        msg /= DHCP6OptOptReq()  # this adds 23 and 24 opt by default, we can leave it that way in this point.

    if world.cfg["add_option"]["relay_msg"]:
        msg /= DHCP6OptRelayMsg()/DHCP6_Solicit()

    if world.cfg["add_option"]["IA_Prefix"]:
        msg /= DHCP6OptIA_PD(iaid = int(world.cfg["values"]["ia_pd"]),
                             T1 = world.cfg["values"]["T1"],
                             T2 = world.cfg["values"]["T2"],
                             iapdopt = DHCP6OptIAPrefix(preflft = world.cfg["values"]["preflft"],
                                 validlft = world.cfg["values"]["validlft"],
                                 plen = world.cfg["values"]["plen"],
                                 prefix = world.cfg["values"]["prefix"]))

    if world.cfg["add_option"]["IA_Address"] and world.cfg["values"]["IA_Address"] != "::":
        world.cfg["add_option"]["IA_NA"] = False
        msg /= DHCP6OptIA_NA(iaid = int(world.cfg["values"]["ia_id"]),
                              T1 = world.cfg["values"]["T1"],
                              T2 = world.cfg["values"]["T2"],
                              ianaopts = DHCP6OptIAAddress(address = world.cfg["values"]["IA_Address"],
                                                          preflft = world.cfg["values"]["preflft"],
                                                          validlft = world.cfg["values"]["validlft"]))

    if world.cfg["add_option"]["vendor_class"]:
        if world.cfg["values"]["vendor_class_data"] == "":
            msg /= DHCP6OptVendorClass(enterprisenum = world.cfg["values"]["enterprisenum"])
        else:
            msg /= DHCP6OptVendorClass(enterprisenum = world.cfg["values"]["enterprisenum"],
                                       vcdata = VENDOR_CLASS_DATA(data = world.cfg["values"]["vendor_class_data"]))

    if world.cfg["add_option"]["vendor_specific_info"]:
        # convert data for world.vendor with code == 1 (option request)
        # that is the only one option that needs converting.
        vendor_option_request_convert()

        # build VENDOR_CPECIDIC_OPTIONs depending on world.vendor:
        vso_tmp = []
        for each in world.vendor:
            vso_tmp.append(VENDOR_SPECIFIC_OPTION(optcode = each[0],
                                                  optdata = each[1]))
        msg /= DHCP6OptVendorSpecificInfo(enterprisenum = world.cfg["values"]["enterprisenum"],
                                          vso = vso_tmp)
        # clear vendor list
        world.vendor = []
    #
    # set all "add_option" True/False values to default.

    if world.cfg["add_option"]["fqdn"]:
        if world.cfg["values"]["FQDN_flags"] is None:
            assert False, "Please define FQDN flags first."

        converted_fqdn = world.cfg["values"]["FQDN_domain_name"]
        msg /= DHCP6OptClientFQDN(flags = str(world.cfg["values"]["FQDN_flags"]),
                                  fqdn = converted_fqdn)

    if world.cfg["add_option"]["client-link-layer-addr"]:
        msg /= DHCP6OptClientLinkLayerAddr(address_type = world.cfg["values"]["address_type"],
                                           lladdr = world.cfg["values"]["link_local_mac_addr"])

    if world.cfg["add_option"]["remote-id"]:
        msg /= DHCP6OptRemoteID(enterprisenum = world.cfg["values"]["enterprisenum"],
                                remoteid = world.cfg["values"]["remote_id"].replace(':', '').decode('hex'))

    if world.cfg["add_option"]["subscriber-id"]:
        msg /= DHCP6OptSubscriberID(subscriberid = world.cfg["values"]["subscriber_id"].replace(':', '').decode('hex'))

    set_options()
    set_values()
    return msg


def build_msg(msg):

    msg = IPv6(dst = world.cfg["address_v6"],
               src = world.cfg["cli_link_local"])/UDP(sport = world.cfg["source_port"],
                                                      dport = world.cfg["destination_port"])/msg

    # get back to multicast address.
    world.cfg["address_v6"] = "ff02::1:2"

    #transaction id
    msg.trid = random.randint(0, 256*256*256)
    world.cfg["tr_id"] = msg.trid

    #add option request if any
    try:
        if len(world.oro.reqopts) > 0:
                msg = add_option_to_msg(msg, world.oro)
    except:
        pass

    #add other options if any
    try:
        if world.oro is not None and len(world.cliopts):
            for opt in world.cliopts:
                msg = add_option_to_msg(msg, opt)
    except:
        pass

    #add all rest options to message.
    msg = client_option(msg)

    return msg


def create_relay_forward(step, level):
    """
    Encapsulate message in relay-forward message.
    """
    #set flag for adding client option client-id which is added by default
    world.cfg["relay"] = True

    # we pretend to be relay-server so we need to listen on 547 port
    world.cfg["source_port"] = 547

    #get only DHCPv6 part of the message
    msg = world.climsg.pop().getlayer(2)
    #from features.init_all import SRV_IPV6_ADDR
    level = int(level)

    #all three values: linkaddr, peeraddr and hopcount must be filled

    tmp = DHCP6_RelayForward(linkaddr = world.cfg["values"]["linkaddr"],
                             peeraddr = world.cfg["values"]["peeraddr"],
                             hopcount = level)/DHCP6OptIfaceId(ifaceid = world.cfg["values"]["ifaceid"])

    #tmp = DHCP6_RelayForward(linkaddr="3000::ffff", peeraddr="::", hopcount = level)

    #  add options (used only when checking "wrong option" test for
    #  relay-forward message. to add some options to relay-forward
    #  you need to put "Client does include opt_name." before "...using
    #  relay-agent encapsulated in 1 level." and after "Client sends SOLICIT message."
    tmp = client_option(tmp)

    #add RelayMsg option
    tmp /= DHCP6OptRelayMsg()
    #message encapsulation
    while True:
        level -= 1
        if not level: break
        tmp /= DHCP6_RelayForward(hopcount = level,
                                  linkaddr =  world.cfg["values"]["linkaddr"],
                                  peeraddr = world.cfg["values"]["peeraddr"])\
               / DHCP6OptIfaceId(ifaceid = world.cfg["values"]["ifaceid"])\
               / DHCP6OptRelayMsg()

    #build full message
    relay_msg = IPv6(dst = world.cfg["address_v6"],
                     src = world.cfg["cli_link_local"])\
                / UDP(sport = world.cfg["source_port"],
                      dport = world.cfg["destination_port"])\
                / tmp/msg

    # in case if unicast used, get back to multicast address.
    world.cfg["address_v6"] = "ff02::1:2"

    world.climsg.append(relay_msg)

    world.cfg["relay"] = False

## ================ BUILD MESSAGE BLOCK END ===================


## ===================================================================
## ================ SEND/RECEIVE MESSAGE BLOCK START =================


def send_wait_for_message(step, type, presence, exp_message):
    """
    Block until the given message is (not) received.
    Parameter:
    new: (' new', optional): Only check the output printed since last time
                             this step was used for this process.
    process_name ('<name> stderr'): Name of the process to check the output of.
    message ('message <message>'): Output (part) to wait for.
    """
    world.cliopts = [] #clear options, always build new message, also possible make it in client_send_msg
    may_flag = False
    #debug.recv = []
    conf.use_pcap = True
    if str(type) in "MUST":
        pass
    elif str(type) in "MAY":
        may_flag = True
    # we needs to get it operational
    # problem: break test with success. (for now we can break test only with fail)
    else:
        assert False, "Invalid expected behavior: %s." % str(type)

    # Uncomment this to get debug.recv filled with all received messages
    conf.debug_match = True
    ans, unans = sr(world.climsg,
                    iface = world.cfg["iface"],
                    timeout = world.cfg["wait_interval"],
                    nofilter = 1,
                    verbose = world.scapy_verbose)

    from features.init_all import SHOW_PACKETS_FROM
    if SHOW_PACKETS_FROM in ['both', 'client']:
            world.climsg[0].show()

    expected_type_found = False
    received_names = ""
    world.srvmsg = []
    for x in ans:
        a, b = x
        world.srvmsg.append(b)

        if SHOW_PACKETS_FROM in ['both', 'server']:
            b.show()

        if not world.loops["active"]:
            get_common_logger().info("Received packet type = %s" % get_msg_type(b))

        received_names = get_msg_type(b) + " " + received_names
        if get_msg_type(b) == exp_message:
            expected_type_found = True

    for x in unans:
        get_common_logger().error(("Unmatched packet type = %s" % get_msg_type(x)))

    if not world.loops["active"]:
        get_common_logger().debug("Received traffic (answered/unanswered): %d/%d packet(s)." % (len(ans), len(unans)))

    if may_flag:
        if len(world.srvmsg) != 0:
            assert True, "Response received."
        if len(world.srvmsg) == 0:
            assert True, "Response not received."  # stop the test... ??
    elif presence:
        assert len(world.srvmsg) != 0, "No response received."
        assert expected_type_found, "Expected message " + exp_message + " not received (got " + received_names + ")"
    elif not presence:
        assert len(world.srvmsg) == 0, "Response received, not expected"


def get_last_response():
    assert len(world.srvmsg), "No response received."
    msg = world.srvmsg[len(world.srvmsg) - 1].copy()
    return msg

## ================ SEND/RECEIVE MESSAGE BLOCK END ===================


## =======================================================================
## ================ PARSING RECEIVED MESSAGE BLOCK START =================

def test_content(value_name):
    # !! probably REMOVE!!
    #this is only beta version of value testing
    if value_name in "address":
        opt = get_option(world.srvmsg[0], 3)
        if str(opt.ianaopts[0].addr[-1]) in [":", "0"]:
            assert False, "Invalid assigned address: %s" % opt.ianaopts[0].addr
    else:
        assert False, "testing %s not implemented" % value_name


def get_msg_type(msg):
    msg_types = {"ADVERTISE": DHCP6_Advertise,
                 "REQUEST": DHCP6_Request,
                 "REPLY": DHCP6_Reply,
                 "RELAYREPLY": DHCP6_RelayReply}

    # 0th is IPv6, 1st is UDP, 2nd should be DHCP6
    dhcp = msg.getlayer(2)

    for msg_name in msg_types.keys():
        if type(dhcp) == msg_types[msg_name]:
            return msg_name

    return "UNKNOWN-TYPE"

# Returns option of specified type


def client_save_option(step, option_name, count = 0):
    assert option_name in options6, "Unsupported option name " + option_name
    opt_code = options6.get(option_name)
    opt = get_option(get_last_response(), opt_code)

    assert opt, "Received message does not contain option " + option_name
    opt.payload = None

    if not count in world.savedmsg:
        world.savedmsg[count] = [opt]
    else:
        world.savedmsg[count].append(opt)


def client_copy_option(step, option_name):
    """
    Copy option from received message
    """
    assert world.srvmsg

    assert option_name in options6, "Unsupported option name " + option_name
    opt_code = options6.get(option_name)

    # find and copy option
    opt = get_option(world.srvmsg[0], opt_code)

    assert opt, "Received message does not contain option " + option_name

    # payload need to be 'None'otherwise we copy all options from one we are
    # looking for till the end of the message
    # it would be nice to remove 'status code' sub-option
    # before sending it back to server
    opt.payload = None
    add_client_option(opt)


def get_option(msg, opt_code):
    # We need to iterate over all options and see
    # if there's one we're looking for

    # message needs to be copied, otherwise we changing original message
    # what makes sometimes multiple copy impossible.
    tmp_msg = msg.copy()

    # clear all opts/subopts
    world.opts = []
    world.subopts = []
    tmp = None
    x = tmp_msg.getlayer(3) # 0th is IPv6, 1st is UDP, 2nd is DHCP6, 3rd is the first option

    # check all message, for expected option and all suboptions in IA_NA/IA_PD
    check_suboptions = {3: 'ianaopts',
                        25: 'iapdopt',
                        17: 'vso'
                        }
    while x:
        if x.optcode == int(opt_code):
            tmp = x
            world.opts.append(x)

        # add IA Address and Status Code as separate option

#        MAKE IT WORK :)
#         for combination in check_suboptions:
#             if x.optcode == combination[0]:
#                 for each in x.fields.get(data_type(combination[1])):
#                     world.subopts.append([number,each])
        if x.optcode == 3:
            for each in x.ianaopts:
                world.subopts.append([3, each])

        # add IA PrefixDelegation and Status Code as separate option
        if x.optcode == 25:
            for each in x.iapdopt:
                world.subopts.append([25, each])
        # add suboptions for vendor specific information
        if x.optcode == 17:
            for each in x.vso:
                world.subopts.append([17, each])
        # add Status Code to suboptions even if it is option in main message
        if x.optcode == 13:
                world.subopts.append([0, x])
        x = x.payload
    return tmp


def unknown_option_to_str(data_type, opt):
    if data_type == "uint8":
        assert len(opt.data) == 1, "Received option " + opt.optcode + " contains " + len(opt.data) + \
                                   " bytes, but expected exactly 1"
        return str(ord(opt.data[0:1]))
    else:
        assert False, "Parsing of option format " + data_type + " not implemented."


def response_check_include_option(step, must_include, opt_code):
    """
    Checking presence of expected option.
    """
    assert len(world.srvmsg) != 0, "No response received."

    opt = get_option(world.srvmsg[0], opt_code)

    if must_include:
        assert opt, "Expected option " + opt_code + " not present in the message."
    else:
        assert opt is None, "Unexpected option " + opt_code + " found in the message."

# Returns text representation of the option, interpreted as specified by data_type


def sub_option_help(expected, opt_code):
    x = []
    received = ''
    for each in world.subopts:
        # we need to be sure that option 13 is in 25 or 3
        # otherwise sub-option 13 from option 3 could be taken
        # as sub-option from option 25. And that's important!
        if each[0] == opt_code:
            if each[1].optcode == expected:
                x.append(each[1])
                received += str(each[1].optcode)
    else:
        assert len(x) > 0, "Expected sub-option " + str(expected) + " not present in the option " + str(opt_code)
        return x, received


def extract_duid(option):
    if option.type == 1:
        # DUID_LLT
        return "00010001" + str(option.timeval) + str(option.lladdr).replace(":", "")
    elif option.type == 2:
        # DUID_EN
        return ("00020001" + str(option.enterprisenum) + str(option.id)).replace(":", "")
    elif option.type == 3:
        # DUID_LL
        return "00030001" + str(option.lladdr).replace(":", "")


def response_check_option_content(step, subopt_code, opt_code, expect, data_type, expected):

    opt_code = int(opt_code)
    subopt_code = int(subopt_code)
    data_type = str(data_type)
    expected = str(expected)
    # without any msg received, fail test
    assert len(world.srvmsg) != 0, "No response received."

    # get that one option, also fill world.opts (for multiple options same type, e.g. IA_NA)
    # and world.subopts for suboptions for e.g. IA Address or StatusCodes
    x = get_option(world.srvmsg[0], opt_code)

    received = ""

    # check sub-options if we are looking for some
    if data_type in "sub-option":
        x, receive_tmp = sub_option_help(int(expected), opt_code)
        received += receive_tmp

    # no option received? Fail test (there is one think to do: optional statuscode(13) in main
    # message, not as a sub-option!
    assert x, "Expected option " + str(opt_code) + " not present in the message."

    # test all collected options,:
    if subopt_code is 0:
        for each in world.opts:
            if opt_code == 1:
                if data_type == "duid":
                    received += extract_duid(each.duid)
                    expected = expected.replace(":", "")
            elif opt_code == 2:
                if data_type == "duid":
                    received += extract_duid(each.duid)
                    expected = expected.replace(":", "")
            # uncomment to print all pocket fields
            #assert False, each.fields.keys()
            elif opt_code == 3:
                # looking for all kinds of variables, specified in test step (e.g. T1 )
                received += str(each.fields.get(data_type))
            elif opt_code == 4:
                received += str(each.fields.get(data_type))
            elif opt_code == 7:
                received = str(each.prefval)
            elif opt_code == 9:
                # receive relay messages bug in scapy must be fixed!
                #each.payload.show()
                #hexdump(each.payload)
                #assert False, 'break'
                received += str(each.fields.get(data_type))
            elif opt_code == 13:
                received = str(each.statuscode)
            elif opt_code == 17:
                received += str(each.fields.get(data_type))
                #received = str(each.enterprisenum)
            elif opt_code == 21:
                received = ",".join(each.sipdomains)
            elif opt_code == 22:
                received = ",".join(each.sipservers)
            elif opt_code == 23:
                received = ",".join(each.dnsservers)
            elif opt_code == 24:
                received = ",".join(each.dnsdomains)
            elif opt_code == 25:
                # looking for all kinds of variables, specified in test step (e.g. T1 )
                # temporary fix until it wont be fixed in scapy
                if data_type == "iapd":
                    data_type = "iaid"
                received += str(each.fields.get(data_type))
            elif opt_code == 27:
                received = ",".join(each.nisservers)
            elif opt_code == 28:
                received = ",".join(each.nispservers)
            elif opt_code == 29:
                received = each.nisdomain
            elif opt_code == 30:
                received = each.nispdomain
            elif opt_code == 31:
                received = ",".join(each.sntpservers)
            elif opt_code == 32:
                received = str(each.reftime)
            elif opt_code == 39:
                received = str(each.fields.get(data_type))

            else:
                # if you came to this place, need to do some implementation with new options
                received = unknown_option_to_str(data_type, each)
    else:
        # test all suboptions which we extracted from received message,
        # and also test primary option for that sub-option.We don't want to have
        # situation when 13 suboption from option 3 was taken as a subotion of option 25.
        # yes that's freaky...
        # each[0] - it's parent optcode (for 26 it will be 25, for 13 it will be 3,
        # some times statuscode option included not as sub-option will be marked as 0.

        for each in world.subopts:
            if each[0] == opt_code:
                if opt_code == 17:
                    received += str(each[1].optdata) + ' '
                    continue
                try:
                    received += str(each[1].payload.fields.get(data_type)) + ' '
                except:
                    pass

    # test if expected option/suboption/value is in all collected options/suboptions/values
    if expect is None or expect is True:
        assert expected in received, "Invalid " + str(opt_code) + " option, received "\
                                     + data_type + ": " + received + ", but expected " + str(expected)
    elif expect is False:
        assert expected not in received, "Received value of " + data_type + ": " + received + \
                                         " should not be equal to value from client - " + str(expected)


def save_value_from_option(step, value_name, option_name):

    assert world.srvmsg
    get_option(world.srvmsg[0], option_name)
    if len(world.opts) == 0:
        temp = world.subopts[0][1].payload
        world.savedvalue = getattr(temp, value_name)
        world.subopts = []
    else:
        world.savedvalue = getattr(world.opts[0], value_name)
        world.opts = []
        world.subopts = []


def compare_values(step, value_name, option_name):

    assert world.srvmsg
    get_option(world.srvmsg[0], option_name)
    if len(world.opts) == 0:
        subopt = world.subopts[0][1].payload
        to_cmp = getattr(subopt, value_name)
        assert world.savedvalue == to_cmp, \
            "Compared values %s and %s do not match" % (world.savedvalue, to_cmp)
        world.subopts = []
    else:
        to_cmp = getattr(world.opts[0], value_name)
        assert world.savedvalue == to_cmp, \
            "Compared values %s and %s do not match" % (world.savedvalue, to_cmp)
        world.opts = []
        world.subopts = []

## ================ PARSING RECEIVED MESSAGE BLOCK END ===================


## =======================================================================
## ==================== TESTING IN LOOPS BLOCK START =====================

def loops_config_sld(step):
    world.loops["save_leases_details"] = True


def values_for_loops(step, value_name, file_flag, values):
    value_name = str(value_name)
    if value_name == "client-id":
        world.loops[value_name] = []
        for each in str(values).split(" "):
            world.cfg["values"]["DUID"] = each
            world.loops[value_name].append(convert_DUID())


def loops(step, message_type_1, message_type_2, repeat):
    import importlib
    testsetup = importlib.import_module("misc")
    repeat = int(repeat)
    testsetup.set_world()
    testsetup.test_procedure(None)

    if repeat < 1000:
        x_range = 10
    else:
        x_range = 250

    world.loops["active"] = True
    world.scapy_verbose = 0

    if message_type_1 == "SOLICIT" and message_type_2 == "ADVERTISE":
        # short two message exchange without saving leases.
        for x in range(0, repeat):
            client_send_msg(step, message_type_1, None, None)
            send_wait_for_message(step, "MAY", True, message_type_2)

    elif message_type_1 == "SOLICIT" and message_type_2 == "REPLY":
        # first save server-id option
        client_send_msg(step, message_type_1, None, None)
        send_wait_for_message(step, "MAY", True, "ADVERTISE")
        client_save_option(step, "server-id")

        # long 4 message exchange with saving leases.
        for x in range(1, repeat):
            # if x % x_range == 0:
            #     get_common_logger().info("Message exchane no. %d", x)
            generate_new(step, "client")
            client_send_msg(step, message_type_1, None, None)
            send_wait_for_message(step, "MAY", True, "ADVERTISE")

            try:
                client_add_saved_option(step, False)
                client_copy_option(step, "IA_NA")
            except AssertionError:
                pass

            client_send_msg(step, "REQUEST", None, None)
            send_wait_for_message(step, "MAY", True, message_type_2)

    elif message_type_1 == "REQUEST" and message_type_2 == "REPLY":
        # first save server-id option
        client_send_msg(step, "SOLICIT", None, None)
        send_wait_for_message(step, "MAY", True, "ADVERTISE")
        client_save_option(step, "server-id")

        # long 4 message exchange with saving leases.
        for x in range(1, repeat):
            if x % x_range == 0:
                get_common_logger().info("Message exchane no. %d", x)
            generate_new(step, "client")
            client_add_saved_option(step, False)
            client_send_msg(step, "REQUEST", None, None)
            send_wait_for_message(step, "MAY", True, message_type_2)
            response_check_option_content(step, 13, 3, "NOT", "statuscode", "2")

    elif message_type_1 == "RELEASE" and message_type_2 == "REPLY":
        # first save server-id option
        client_send_msg(step, "SOLICIT", None, None)
        send_wait_for_message(step, "MAY", True, "ADVERTISE")
        client_save_option(step, "server-id")

        # long 4 message exchange with saving leases.
        for x in range(1, repeat):
            if x % x_range == 0:
                get_common_logger().info("Message exchane no. %d", x)

            client_add_saved_option(step, False)
            client_send_msg(step, "REQUEST", None, None)
            send_wait_for_message(step, "MAY", True, message_type_2)

            client_add_saved_option(step, False)
            client_copy_option(step, "IA_NA")
            client_send_msg(step, "RELEASE", None, None)
            send_wait_for_message(step, "MAY", True, message_type_2)
            #dhcpmsg.generate_new(step, "client")

    else:
        pass
    for x in range(0, len(world.savedmsg)):
        world.savedmsg[x] = []


def save_info():
    pass