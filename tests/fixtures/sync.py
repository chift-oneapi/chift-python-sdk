READ_SYNC_ALL = [
    {
        "name": "Migrate your accounting data to Qonto",
        "syncid": "76d8b868-4900-4302-9eee-c3d62bb79b2d",
        "consumers": [],
        "connections": [
            {"connection_type": 7015, "display_order": 0, "display_hidden": True},
            {"one_api": 200, "display_order": 1, "display_hidden": False},
        ],
        "mappings": [],
        "flows": [
            {
                "id": "flow-1",
                "name": "Migration de la comptabilité vers Qonto",
                "description": "Migrer facilement vos données depuis n'importe quelle plateforme",
                "triggers": [{"id": "trigger-1", "type": "event"}],
                "execution": {
                    "type": "module",
                    "data": {"name": "Accounting to Qonto Migration"},
                },
                "config": {
                    "datastores": [
                        {
                            "name": "INVOICES",
                            "definition": {
                                "columns": [
                                    {
                                        "name": "source_id",
                                        "type": "text",
                                        "title": "Invoice source id",
                                    },
                                    {
                                        "name": "target_id",
                                        "type": "text",
                                        "title": "Invoice target id",
                                    },
                                    {
                                        "name": "reference",
                                        "type": "text",
                                        "title": "Invoice code/ref",
                                    },
                                ],
                                "search_column": "source_id",
                            },
                        },
                        {
                            "name": "CONTACTS",
                            "definition": {
                                "columns": [
                                    {
                                        "name": "source_id",
                                        "type": "text",
                                        "title": "Contact source id",
                                    },
                                    {
                                        "name": "target_id",
                                        "type": "text",
                                        "title": "Contact target id",
                                    },
                                ],
                                "search_column": "source_id",
                            },
                        },
                        {
                            "name": "SYNC_ALL_SUCCESSFUL",
                            "definition": {
                                "columns": [
                                    {
                                        "name": "first_execution_completed",
                                        "type": "bool",
                                        "title": "Has first execution (contact import) completed successfully",
                                    }
                                ]
                            },
                        },
                        {
                            "name": "SYNC_ALL_ATTEMPTS",
                            "definition": {
                                "columns": [
                                    {
                                        "name": "attempt",
                                        "type": "integer",
                                        "title": "Failure attempt number",
                                    }
                                ]
                            },
                        },
                        {
                            "name": "ERRORS",
                            "definition": {
                                "columns": [
                                    {"name": "model", "type": "text", "title": "Model"},
                                    {
                                        "name": "source_id",
                                        "type": "text",
                                        "title": "Source id",
                                    },
                                    {
                                        "name": "reference",
                                        "type": "text",
                                        "title": "Reference",
                                        "optional": True,
                                    },
                                    {
                                        "name": "message",
                                        "type": "text",
                                        "title": "Error message",
                                    },
                                    {
                                        "name": "detail",
                                        "type": "text",
                                        "title": "Error detail",
                                        "optional": True,
                                    },
                                    {
                                        "name": "error_code",
                                        "type": "text",
                                        "title": "Error code",
                                        "optional": True,
                                    },
                                ]
                            },
                        },
                    ],
                    "definitionFields": [],
                    "customFields": [{"type": "target_node_id", "value": 7015}],
                },
            }
        ],
    },
    {
        "name": "Agicap Banking -> Comptabilité",
        "syncid": "76d8b868-4900-4302-9eee-c3d62bb79b2d",
        "consumers": [],
        "connections": [
            {
                "one_api": None,
                "connection_type": 4014,
                "display_order": 0,
                "display_hidden": False,
            },
            {
                "one_api": 200,
                "connection_type": None,
                "display_order": 1,
                "display_hidden": False,
            },
        ],
        "mappings": [
            {
                "name": "Journal",
                "description": "Sélectionnez le journal de banque à utiliser pour la création des écritures comptables",
                "logic": None,
                "display_order": 2,
                "sub_mappings": [
                    {
                        "name": "Journal",
                        "source_field": {
                            "name": "Journal",
                            "type": "fixed",
                            "display_condition": None,
                            "values": [
                                {
                                    "id": "bank_journal",
                                    "label": "Journal de banque à utiliser",
                                }
                            ],
                            "api_route": None,
                            "connection_type": None,
                        },
                        "target_field": {
                            "name": "Journaux comptables",
                            "type": "api",
                            "display_condition": {
                                "in": [
                                    {"var": "journal_type"},
                                    ["financial_operation", "unknown"],
                                ]
                            },
                            "values": None,
                            "api_route": "accounting/journals",
                            "connection_type": None,
                        },
                        "display_delete": False,
                        "display_order": 0,
                    }
                ],
            },
            {
                "name": "Comptes comptables",
                "description": "Mappez les comptes comptables à utiliser par défaut",
                "logic": None,
                "display_order": 3,
                "sub_mappings": [
                    {
                        "name": "Comptes comptables",
                        "source_field": {
                            "name": "Type de compte",
                            "type": "fixed",
                            "display_condition": None,
                            "values": [
                                {
                                    "id": "bank_account",
                                    "label": "Compte de banque par défaut",
                                },
                                {
                                    "id": "collective_supplier",
                                    "label": "Compte collectif des fournisseurs",
                                },
                            ],
                            "api_route": None,
                            "connection_type": None,
                        },
                        "target_field": {
                            "name": "Comptes comptables",
                            "type": "api",
                            "display_condition": None,
                            "values": None,
                            "api_route": "accounting/chart-of-accounts/45",
                            "connection_type": None,
                        },
                        "display_delete": False,
                        "display_order": 0,
                    }
                ],
            },
        ],
        "flows": [
            {
                "name": "Export bancaire vers la comptabilité",
                "id": "flow-2",
                "description": "Export automatique des transactions bancaires vers la comptabilité",
                "triggers": [
                    {
                        "id": "trigger-1",
                        "type": "timer",
                        "cronschedules": ["0 5 * * *"],
                    },
                    {
                        "id": "trigger-2",
                        "type": "timer",
                        "cronschedules": ["0 12 * * *"],
                    },
                    {
                        "id": "trigger-3",
                        "type": "timer",
                        "cronschedules": ["0 19 * * *"],
                    },
                ],
                "execution": {
                    "type": "module",
                    "data": {"name": "Agicap Banking to accounting"},
                },
                "config": {
                    "definitionFields": [
                        {
                            "name": "from_date",
                            "type": "date",
                            "title": "Début de la synchronisation? (dd/mm/yyyy). Uniquement les transactions exportées "
                            "à partir de la date sélectionnée seront traitées",
                            "optional": False,
                        },
                        {
                            "data": [
                                {"title": "Oui", "value": "yes"},
                                {"title": "Non", "value": "no"},
                            ],
                            "name": "draft_invoices",
                            "type": "select",
                            "title": "Voulez-vous créer les écritures en brouillon/attente ? (Ceci n'est pas possible "
                            "pour tous les logiciels de production et n'aura dans ce cas pas d'impact sur la "
                            "synchronisation)",
                            "default": "yes",
                            "optional": False,
                        },
                        {
                            "data": [
                                {
                                    "title": "Titre de la transaction sur toutes les lignes",
                                    "value": "lines_with_title",
                                },
                                {
                                    "title": "Nom du fournisseur sur toutes les lignes",
                                    "value": "lines_with_partner_name",
                                },
                                {
                                    "title": "Nom du fournisseur ET titre de la transaction sur toutes les lignes",
                                    "value": "lines_with_both",
                                },
                            ],
                            "name": "line_descriptions_mode",
                            "type": "select",
                            "title": "Libellé des écritures",
                            "default": "lines_with_title",
                            "optional": False,
                        },
                    ],
                    "doorkeyFields": None,
                    "customFields": [
                        {
                            "type": "accounting_journals_mapping_name",
                            "value": "Journal",
                        },
                        {
                            "type": "accounting_accounts_mapping_name",
                            "value": "Comptes comptables",
                        },
                        {"type": "DATES", "value": "DATES"},
                        {"type": "TRANSACTIONS", "value": "Synced transactions"},
                        {"type": "SUPPLIERS", "value": "Synced suppliers"},
                        {"type": "ERRORS", "value": "Synced errors"},
                    ],
                    "datastores": [
                        {
                            "name": "Synced transactions",
                            "definition": {
                                "columns": [
                                    {
                                        "name": "transaction_id",
                                        "title": "Agicap ID",
                                        "type": "text",
                                        "optional": False,
                                    },
                                    {
                                        "name": "accounting_id",
                                        "title": "Accounting ID",
                                        "type": "text",
                                        "optional": False,
                                    },
                                    {
                                        "name": "agicap_number",
                                        "title": "Agicap number",
                                        "type": "text",
                                        "optional": False,
                                    },
                                    {
                                        "name": "accounting_number",
                                        "title": "Entry number",
                                        "type": "text",
                                        "optional": False,
                                    },
                                    {
                                        "name": "date_synced",
                                        "title": "Date",
                                        "type": "text",
                                        "optional": False,
                                    },
                                ],
                                "search_column": "purchase_id",
                            },
                        },
                        {
                            "name": "Synced suppliers",
                            "definition": {
                                "columns": [
                                    {
                                        "name": "supplier_id",
                                        "title": "Id (agicap)",
                                        "type": "text",
                                        "optional": False,
                                    },
                                    {
                                        "name": "accounting_supplier_id",
                                        "title": "Id (accounting)",
                                        "type": "text",
                                        "optional": False,
                                    },
                                    {
                                        "name": "date_synced",
                                        "title": "Date",
                                        "type": "text",
                                        "optional": False,
                                    },
                                ],
                                "search_column": "supplier_id",
                            },
                        },
                        {
                            "name": "Synced errors",
                            "definition": {
                                "columns": [
                                    {
                                        "name": "message",
                                        "title": "Error message",
                                        "type": "text",
                                        "optional": False,
                                    }
                                ],
                                "search_column": None,
                            },
                        },
                        {
                            "name": "DATES",
                            "definition": {
                                "columns": [
                                    {"name": "date", "type": "text", "title": "Date"}
                                ]
                            },
                        },
                    ],
                },
            }
        ],
    },
]
