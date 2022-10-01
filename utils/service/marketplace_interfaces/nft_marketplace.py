from abc import ABC, abstractmethod
from pyteal import *
import algosdk

class NFTMarketplaceInterface(ABC):

    @abstractmethod
    def initialize_escrow(self, escrow_address):
        curr_escrow_address = App.globalGetEx(Int(0), self.Variables.escrow_address) 

        asset_escrow = AssetParam.clawback(Txn.assets[0])
        manager_address = AssetParam.manager(Txn.assets[0])
        freeze_address = AssetParam.freeze(Txn.assets[0])
        reserve_address = AssetParam.reserve(Txn.assets[0])
        default_frozen = AssetParam.defaultFrozen(Txn.assets[0])

        return Seq([
            curr_escrow_address,
            Assert(curr_escrow_address.hasValue() == Int(0)), 

            Assert(App.globalGet(self.Variables.app_admin) == Txn.sender()),
            Assert(Global.group_size() == Int(1)),

            asset_escrow,
            manager_address,
            freeze_address,
            reserve_address,
            default_frozen,
            Assert(Txn.assets[0] == App.globalGet(self.Variables.asa_id)),
            Assert(asset_escrow.value() == Txn.application_args[1]),
            Assert(default_frozen.value()),
            Assert(manager_address.value() == Global.zero_address()),
            Assert(freeze_address.value() == Global.zero_address()),
            Assert(reserve_address.value() == Global.zero_address()),

            App.globalPut(self.Variables.escrow_address, escrow_address),
            App.globalPut(self.Variables.app_state, self.AppState.active),
            Return(Int(1))
        ])

    @abstractmethod
    def make_sell_offer(self, sell_price):
        valid_number_of_transactions = Global.group_size() == Int(1)
        app_is_active = Or(App.globalGet(self.Variables.app_state) == self.AppState.active,
                           App.globalGet(self.Variables.app_state) == self.AppState.selling_in_progress)

        valid_seller = Txn.sender() == App.globalGet(self.Variables.asa_owner)
        valid_number_of_arguments = Txn.application_args.length() == Int(2)

        can_sell = And(valid_number_of_transactions,
                       app_is_active,
                       valid_seller,
                       valid_number_of_arguments)

        update_state = Seq([
            App.globalPut(self.Variables.asa_price, Btoi(sell_price)),
            App.globalPut(self.Variables.app_state, self.AppState.selling_in_progress),
            Return(Int(1))
        ])

        return If(can_sell).Then(update_state).Else(Return(Int(0)))

    @abstractmethod
    def buy(self):
        valid_number_of_transactions = Global.group_size() == Int(3)
        asa_is_on_sale = App.globalGet(self.Variables.app_state) == self.AppState.selling_in_progress

        valid_payment_to_seller = And(
            Gtxn[1].type_enum() == TxnType.Payment,
            Gtxn[1].receiver() == App.globalGet(self.Variables.asa_owner), # correct receiver
            Gtxn[1].amount() == App.globalGet(self.Variables.asa_price), # correct amount 
            Gtxn[1].sender() == Gtxn[0].sender(), # equal sender of the first two transactions, which is the buyer
            Gtxn[1].sender() == Gtxn[2].asset_receiver() # correct receiver of the NFT
        )

        valid_asa_transfer_from_escrow_to_buyer = And(
            Gtxn[2].type_enum() == TxnType.AssetTransfer,
            Gtxn[2].sender() == App.globalGet(self.Variables.escrow_address),
            Gtxn[2].xfer_asset() == App.globalGet(self.Variables.asa_id),
            Gtxn[2].asset_amount() == Int(1)
        )

        can_buy = And(valid_number_of_transactions,
                      asa_is_on_sale,
                      valid_payment_to_seller,
                      valid_asa_transfer_from_escrow_to_buyer)

        update_state = Seq([
            App.globalPut(self.Variables.asa_owner, Gtxn[0].sender()), # update the owner of the ASA.
            App.globalPut(self.Variables.app_state, self.AppState.active), # update the app state
            Return(Int(1))
        ])

        return If(can_buy).Then(update_state).Else(Return(Int(0)))

    @abstractmethod
    def stop_sell_offer(self):
        valid_number_of_transactions = Global.group_size() == Int(1)
        valid_caller = Txn.sender() == App.globalGet(self.Variables.asa_owner)
        app_is_initialized = App.globalGet(self.Variables.app_state) != self.AppState.not_initialized

        can_stop_selling = And(valid_number_of_transactions,
                               valid_caller,
                               app_is_initialized)

        update_state = Seq([
            App.globalPut(self.Variables.app_state, self.AppState.active),
            Return(Int(1))
        ])

        return If(can_stop_selling).Then(update_state).Else(Return(Int(0)))
