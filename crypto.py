import discord 
from discord.ext import commands
from pycoingecko import CoinGeckoAPI

class crypto(commands.Cog):
  def __init__(self, client):
    self.cg = CoinGeckoAPI()
    self.currency = 'usd'
    self.coin_list = self.cg.get_coins_markets(self.currency)

  @commands.command()
  async def price(self, ctx, inp):
    sen = self.find_price(inp)
    
    await ctx.send(f'${sen}')

  @commands.command()
  async def mc(self, ctx, inp):
    sen = format(self.find_mc(inp), ',d')
    await ctx.send(f'${sen}')

  @commands.command(aliases = ['24$'])
  async def _24dollar(self, ctx, inp):
    sen = self.day_change(inp,'$')

    await ctx.send(f'${sen}')

  @commands.command(aliases = ['24%'])
  async def _24percentage(self, ctx, inp):
    sen = self.day_change(inp, '%')

    await ctx.send(f'%{sen}')

  def find_price(self,inp):
    if len(inp) >4:
      res = self.cg.get_price(inp, 'usd')[inp][self.currency]
    else:
      res = self.find_ticker_price(inp)
    return res

  def find_ticker_price(self, inp):
      for i in range (len(self.coin_list)):
        if self.coin_list[i]['symbol'] == inp:
          return self.coin_list[i]['current_price']
        
      return ('Could not find that one')

  def find_mc(self,inp):
      for i in range (len(self.coin_list)):
        if self.coin_list[i]['symbol'] == inp or self.coin_list[i]['id'] == inp :
          return self.coin_list[i]['market_cap']

      return ('Could not find that one')

  def day_change(self,inp, query):
    for i in range (len(self.coin_list)):
      if query == '$':
        if self.coin_list[i]['symbol'] == inp or self.coin_list[i]['id'] == inp:
          return self.coin_list[i]['price_change_24h']

      if query == '%':
        if self.coin_list[i]['symbol'] == inp or self.coin_list[i]['id'] == inp:
          return self.coin_list[i]['price_change_percentage_24h']

    return ('Could not find that one')

  @commands.command()
  async def dev(self, ctx):
    await ctx.send('Currently working on personal and channel price alerts')

  @commands.command()
  async def help(self, ctx):
    out = "Use '$' Prefix before any command \n \n Commands: \n \n'price' returns current price \n \n'mc' returns current market cap \n \n'24$' and '24%' returns the 24 hour change respectively \n \nUse 'dev' to currently see whats currently in development \n \nCredits: ZaidAj11"
    await ctx.send("```\n" + out+ "\n```")

  @commands.command()
  async def compare(self, ctx, coin1, coin2):
    for i in range (len(self.coin_list)):
      
      if self.coin_list[i]['symbol'] == coin1 or self.coin_list[i]['id'] == coin1:
        coin1_val = self.coin_list[i]['price_change_percentage_24h']
      if self.coin_list[i]['symbol'] == coin2 or self.coin_list[i]['id'] == coin2:
        coin2_val = self.coin_list[i]['price_change_percentage_24h']
    if(coin1_val<coin2_val):
      temp = coin1
      coin1 = coin2
      coin2 = temp
      temp = coin1_val
      coin1_val = coin2_val
      coin2_val = temp
    differnce = ((coin1_val - coin2_val)/ coin2_val)
    await ctx.send(f'{coin1} outperformed {coin2} by %{differnce}')


 

def setup(client):
  client.add_cog(crypto(client))