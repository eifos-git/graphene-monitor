from peerplays.proposal import Proposals
from peerplays.account import Account
from . import AbstractSource
import json


class Proposal(AbstractSource):
    """Get a list of all active proposals on the blockchain from one user. Config settings:

        * account_name: <account_name>

    Returns all active proposals as list of dictionaries with the following keys:
        * proposal_id
        * expiration_time
    """
    def get_witness_account(self):
        return self._get_config_value("account_name")

    def retrieve_data(self):
        account = self.get_witness_account()
        proposals = Proposals(account)
        # list of open proposals
        proposals.refresh()
        proposals = Proposals(account)

        data = []
        for proposal in proposals:
            if proposal.proposer:
                proposer = Account(proposal.proposer)["name"]
            else:
                proposer = "n/a"

            data.append(dict(
                    proposal_id=proposal["id"],
                    expiration_time=proposal["expiration_time"],
           #         proposer,
           #         [
           #             Account(x)["name"]
           #             for x in (
           #                 proposal["required_active_approvals"]
           #                 + proposal["required_owner_approvals"]
           #         )
           #         ],
           #         json.dumps(
           #             [Account(x)["name"] for x in proposal["available_active_approvals"]]
           #             + proposal["available_key_approvals"]
           #             + proposal["available_owner_approvals"],
           #             indent=1,
           #         ),
           #         proposal.get("review_period_time", None),
           #         json.dumps(proposal["proposed_transaction"], indent=4),
            ))
        self._set_data(data)


