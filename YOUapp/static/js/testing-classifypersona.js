$(document).ready(function() {
    $.ajax({
        url: '/ajax/identify_persona/',
        type : "POST",
        data: {
            'targetDB': sessionStorage.getItem('targetDB') + ''
        },
        dataType: 'json',
        success: function (data) {
            result = "";
              $.each(data, function(k, v) {
                result += k + " , " + v + "\n";
              });
             console.log(result)
            alert("STEP 2 DONE! Identified personas!");
        }
    });

});
