$(function() {
  $(document).ready(function() {
    $('#translate').button().click(function() {
      console.log($('#src').val())
      util.getJson(
        '/yukkuri_translator/json/translate',
        {src: $('#src').val()},
        function (errCode, result) {
          console.log(result);
          $('#result').empty();
          $('#result').append(result);
        },
        function() {
          $.blockUI({ message: '<img src="/yukkuri_translator/img/loading.gif" />' });
        },
        function() {
          $.unblockUI();
        }
      );
    });
  });

});
