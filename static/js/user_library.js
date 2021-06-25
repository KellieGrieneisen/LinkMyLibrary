"use strict";



// toggle value for have-read in database by targeting checkbox
// and changing on click via server route commands and queries.
$('.read').on('click', (evt) =>{
  
    const bookId = $(evt.target).data('bookId');

    console.log(`Making request for book ID: ${bookId}`);

    $.post(`/set-read-status/${bookId}`, (res) => {
      console.log(`The book's status is now ${res.have_read}`);
      
    });
});

// for all bootstraps with a popver toggle, trigger popover on click
// and view summary of book.

let popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  let popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
  return new bootstrap.Popover(popoverTriggerEl)
})

// hide contents  of second api call until next page is triggered
$('#page2').hide()


// when clicking next <a> tag, hide page 1 results and show page 2 results
  $('.next').on('click', (evt) =>{
  
    console.log(`Making request for next page of book results`);
    $('#page1').hide()
    $('#page2').show()
    
  });


// when clicking prev <a> tag, hide page 2 results again and continue viewing
// page ones results.
  $('.prev').on('click', (evt) =>{
  
    console.log(`Making request for previous page of book results`);
    $('#page2').hide()
    $('#page1').show()
    
  });

// }

