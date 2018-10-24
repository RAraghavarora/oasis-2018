var config = {
    apiKey: "AIzaSyCkehNgOS7oZ4oE5JNnNR7LDfY4wqDxQW0",
    "authDomain": "vendorapp-80efa.firebaseio.com",
	"databaseURL": "https://vendorapp-80efa.firebaseio.com",
    "storageBucket": "vendorapp-80efa.appspot.com",
};
firebase.initializeApp(config);
var database = firebase.database();
var rows = Array.from($('.order'));

rows.forEach((e)=>{
    var ref = database.ref('/stall/' + e.getAttribute('data-ref'));
    console.log(e.getAttribute('data-ref'))
    console.log(ref);
    ref.on('value', function(snap){
        console.log(snap);
        console.log("chinmay");
        console.log("ready",snap.val().order_ready);
        console.log("complete",snap.val().order_complete);
        console.log("cancelled",snap.val().cancelled);
        if(snap.val().cancelled == true)
            e.querySelectorAll('.updatevalue')[0].innerText = "CANCELLED";
        else if(snap.val().order_complete == true)
            e.querySelectorAll('.updatevalue')[0].innerText = "COMPLETED";
        else if(snap.val().order_ready == true)
            e.querySelectorAll('.updatevalue')[0].innerText = "READY";
        else
            e.querySelectorAll('.updatevalue')[0].innerText = "PENDING";
    })
})





