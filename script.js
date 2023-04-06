/* javascript to accompany jquery.html */

$(document).ready(
   /* this defines a function that gets called after the document is in memory */
  function()
  {
      // click handler for uploadSDF button
      $('#btnInsMol').click(function() {      
         // post request
         const fileName = $('#fileSdf')[0].files[0]
         const molName= $('#formMolName').val()

         const form = new FormData()

         form.append("fileInfo", fileName)
         form.append("mol", molName)

         $.ajax({
            url: 'uploadSDF',
            type: 'POST',
            data: form,
            contentType: false,
            processData: false,
            success: function() {
              // Handle success here
              alert("Success");
            },
            error: function() {
              // Handle error here
              alert("Error");
            }
          });
       });
       
  }
);