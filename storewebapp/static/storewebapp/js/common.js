var BASE_URL = "https://bits-oasis.org/2018/shop";
var WALLET_TOKEN ="JQZ6mq68'MYNa&RNMv/4^mA";
function processResponse (response) {
    var status = response.status;
    var json = response.json();

    return Promise.all([status, json]).then(
        res => ({
            status: res[0],
            json: res[1]
        })
    );
}