/* javascript to accompany jquery.html */

$(document).ready(
   /* this defines a function that gets called after the document is in memory */
  function()
  {
      // click handler for uploadSDF button
      $('#btnInsMol').click(function() {
         var fileInputValue = $('#fileSdf').val();
         var formMolNameValue = $('#formMolName').val();
       
         console.log('fileInputValue:', fileInputValue);
         console.log('formMolNameValue:', formMolNameValue);


         var data = [fileInputValue, formMolNameValue];
       
         // post request
         $.ajax({
            url: 'uploadSDF',
            type: 'POST',
            data: JSON.stringify(data),
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