function getWord(element, winePair){

    main = document.getElementById("main")

    if (winePair){
        wine = element.innerHTML;
        food = main.innerHTML;
    }
    else{
        wine = main.innerHTML;
        food = element.innerHTML;
    }

    $.ajax({
        method: 'GET',
        url: '/history',
        data: {"wine":wine, "food":food},
        success: function(err, req, resp) {
            pairid = resp["responseJSON"]["pairid"];
            console.log('/pairing/' + pairid);
            window.location.href = '/pairing/' + pairid;
        }
    });

}

function selectSearch(){
    var select = document.getElementById("selector").value;
    if(select=="Wine")
    {
        document.getElementById("foodsubmit").style.display = "none";
        document.getElementById("winesubmit").style.display = "block";
    }
    else if (select=="Food"){
        document.getElementById("foodsubmit").style.display = "block";
        document.getElementById("winesubmit").style.display = "none";
    }
}