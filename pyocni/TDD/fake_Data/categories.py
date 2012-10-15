
import pyocni.pyocni_tools.uuid_Generator as uuid

def get_a_kind():

    create_kind =\
        "{"\
        "\"kinds\": ["\
                "{"\
                "\"term\": \"compute\","\
                """
                "scheme": "http://schemas.ogf.org/occi/infrastructure#",
                "title": "Compute Resource",
                "attributes": {
                    "occi": {
                        "compute": {
                            "hostname": {
                                "mutable": true,
                                "required": false,
                                "type": "string",
                                "pattern": "(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\\\-]*[a-zA-Z0-9])\\\\.)*",
                                "minimum": "1",
                                "maximum": "255"
                            },
                            "state": {
                                "mutable": false,
                                "required": false,
                                "type": "string",
                                "pattern": "inactive|active|suspended|failed",
                                "default": "inactive"
                            }
                        }
                    }
                },
                "actions": [
                    "http://schemas.ogf.org/occi/infrastructure/compute/action#start"
                ],
                """ \
                "\"location\": \"/compute\""\
            "}"\
        "]"\
    "}"
    return create_kind

def get_a_mixin():

    mixin = """
{
    "mixins": [
        {
            "term": "medium",
            "scheme": "http://example.com/template/resource#",
            "title": "Medium VM",
            "attributes": {
                "occi": {
                    "compute": {
                        "speed": {
                            "type": "number",
                            "default": 2.8
                        }
                    }
                }
            },
            "location": "/template/resource/medium/"
        }
    ]
}

"""
    return mixin
def get_an_action():

    action =\
    """
                {
                    "actions": [
            {
                "term": "start",
                "scheme": "http://schemas.ogf.org/occi/infrastructure/compute/action#",
                "title": "Start Compute instance",
                "attributes": {
                    "method": {
                        "mutable": true,
                        "required": false,
                        "type": "string",
                        "pattern": "graceful|acpion|poweron",
                        "default": "poweron"
                    }
                }
            }
        ]
    }
    """
    return action

#=======================================================================================================================
put_provider ="""
    {
    "providers": [
            {
            "Provider": {
                "local": [
                    "dummy"
                ],
                "remote": [
                    "Bilel"
                ]
            },
            "OCCI_ID": "http://schemas.ogf.org/occi/infrastructure#compute"
        }
    ]
}
"""

provider_up = """
{
    "Providers": {
        "remote": [],
        "local": [
            "dummy"
        ]
    }
}"""

#======================================================================================================================

post_http_categories = "Category : my_stuff;\"" \
                    "scheme=\"http://example.com/occi/my_stuff#\";"\
                   "class=\"mixin\";"\
                   "title=\"Storage Resource\";"\
                   "location=\"/my_stuff/\";"\
                   "attributes=\"occi.storage.size{required} occi.storage.state{immutable}\";"\
