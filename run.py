
import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from metaapi_cloud_sdk import MetaApi
from metaapi_cloud_sdk.clients.meta_api_client import MetaApiClient
from metaapi_cloud_sdk.clients.meta_api_client import MarketTrade

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define the forward function
def forward(update, context):
    # Get the message from the source channel
    message = update.message
    # Forward the message to the destination channel using your bot
    context.bot.forward_message(chat_id='@destination_channel', from_chat_id='@source_channel', message_id=message.message_id)
    # Place a trade on MetaAPI using the message received from the source channel
    api_token = os.environ['META_API_TOKEN']
    account_id = os.environ['META_API_ACCOUNT_ID']
    symbol = 'EURUSD'
    trade_type = 'MARKET'
    volume = 0.01
    stop_loss = 1.2
    take_profit = 1.4
    client = MetaApiClient(api_token)
    account_information = client.get_account(account_id)
    if account_information.state != 'DEPLOYED':
        raise Exception('The account is not deployed')
    if not account_information.connection_status.connected:
        raise Exception('The account is not connected to broker')
    if not account_information.connection_status.trading_permitted:
        raise Exception('The account is not permitted for trading')
    trade = MarketTrade()
    trade.symbol = symbol
    trade.type = trade_type
    trade.volume = volume
    trade.stop_loss = stop_loss
    trade.take_profit = take_profit
    client.create_trade(account_id, trade)

# Define the main function
def main():
    # Create an instance of the Updater class and pass in your bot's API token
    updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'], use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add a handler for forwarding messages and placing trades on MetaAPI
    dispatcher.add_handler(MessageHandler(Filters.chat('@source_channel'), forward))

    # Start the bot
    updater.start_polling()

if __name__ == '__main__':
    main()
