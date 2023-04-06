/* javascript to accompany jquery.html */

$(document).ready(
   /* this defines a function that gets called after the document is in memory */
  function()
  {
      // click handler for uploadSDF button
      $('#btnInsMol').click(function() {      
         // post request
         $.ajax({
            url: 'uploadSDF',
            type: 'POST',
            data: {
               fileName: $('#fileSdf')[0].files[0],
               molName: $('#formMolName').val()
            },
            contentType: false,
            processData: false,
            success: function(response) {
              // Handle success here
              alert("Success");
            },
            error: function(xhr, status, error) {
              // Handle error here
              alert("Error");
            }
          });
       });
       
  }
);