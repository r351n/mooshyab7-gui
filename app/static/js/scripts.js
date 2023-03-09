$.ajax({
    url: '/search',
    method: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({id: idNum}),
    success: function(response) {
      // Handle the response here
    }
  });
