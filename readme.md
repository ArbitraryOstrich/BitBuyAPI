BitBuy provides an API with a java example. Not knowing java very well I spent a few days tinkering with the example to get it to work then working to get that into python.

I noticed others had tried to do the same so I figured id post.

Specifically [banhao](https://github.com/banhao/BitBuy-API-Authentication-Python) on github and then a few commenst in reddit with no code.

<img alt="readme-2776209b.png" src="assets/readme-2776209b.png" width="" height="" >

This is me just building a component of a system that will graph my balances for me.


Includes some influxDB code to push it into my DB

Includes systemD service files to run the script, note it currently runs every 5
minutes and you may have to change the path.

```sh
sudo ln -s /opt/BitBuyAPI/bitbuy_api.service /etc/systemd/system/bitbuy_api.service
sudo ln -s /opt/BitBuyAPI/bitbuy_api.timer /etc/systemd/system/bitbuy_api.timer
sudo systemctl daemon-reload
```
