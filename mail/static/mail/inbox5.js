document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
  
}

function load_mailbox(mailbox) {

  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  load_mails(mailbox)
}

// Load next set of mails
function load_mails(mailbox) {

  // Get new mails and add mails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(data => {

    // if (mailbox == 'archive') {

    //   data.forEach( data.archived ? data => add_mails(data, mailbox) : null );

    // } else if (mailbox == 'inbox') {

    //   data.forEach( !data.archived ? data => add_mails(data, mailbox) : null );

    // } else {
      
    // }

    data.forEach( data => add_mails(data, mailbox) );

  });

};

// Add a new mail with given contents to DOM
function add_mails(contents, mailbox) {

  // Create mail div
  const mail = document.createElement('div');
  mail.className = 'data-mail';
  mail.id = 'mail-div';
  mail.innerHTML = `<div class="sender-div">${contents.sender}</div>` + 
                    `<div class="subject-div">${contents.subject}</div>` +
                    `<div class="timestamp-div">${contents.timestamp}</div>`;
        
  // To make sure mailbox 'sent' won't appear the icon.
  if (mailbox == 'inbox') {

    // Judge whether the 'tick' icon should be solid or regular
    if (contents.read == true ) {
      mail.innerHTML += `<i class="fas fa-check-circle"></i>`;
    } else {
      mail.innerHTML += `<i class="far fa-check-circle"></i>`;
    }

  }

  // Add mail to DOM
  document.querySelector('#emails-view').append(mail);

  // Add listener to DOM
  mail.addEventListener('click', () => view_mails(contents.id));

};

function view_mails(mail_id) {

  document.querySelector('#content-view').innerHTML = '';

  // Show mail content view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#content-view').style.display = 'block';
    
  fetch(`/emails/${mail_id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    console.log(email);

    // Create mail content div
    const content = document.createElement('div');
    content.className = 'content-row';
    content.innerHTML = `<div class="content-from-div"><span>From:</span><span>${email.sender}</span></div>` + 
                        `<div class="content-subject-div"><span>Subject:</span><span>${email.subject}</span></div>` + 
                        `<div class="content-body-div">
                            <div class="content-body-div-sub">${email.body}</div>
                            <div class="content-date-div">${email.timestamp}</div>
                        </div>`;
    
    // If the email is archived, archived = true.
    if (email.archived) {

      content.innerHTML +=  `<div class="content-func-div">
                            <button class="btn btn-sm btn-outline-primary func-btn" id="content-archive">Unarchive</button>
                            </div>`;
    
    } else {
      
      content.innerHTML +=  `<div class="content-func-div">
                            <button class="btn btn-sm btn-outline-primary func-btn" id="content-archive">Archive</button>
                            <button class="btn btn-sm btn-outline-primary func-btn" id="content-reply">Reply</button>
                            </div>`;
    }
      
    // Add content to DOM
    document.querySelector('#content-view').append(content);
    
    // Add click listener to the button archive
    document.querySelector('#content-archive').addEventListener('click', () => archive_mails(email));

    if (email.read == false) {
      fetch(`/emails/${mail_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    } 
  }); 
}


function archive_mails(contents) {

  if (contents.archived == false) {

    fetch(`/emails/${contents.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })

  } else {

    fetch(`/emails/${contents.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: false
      })
    })

  }

  // Use reload becoz the whole page needs a reload in order to show the lastest mail list.
  // When reload, the DOMContent will be loaded once, after that by default,
  // load_mailbox('inbox') will be called at the top of this script file.

  window.location.reload();
  // load_mailbox('inbox');
  
}

function submit_mails() {

  // Retrieve the values
  var recipients = document.querySelector('#compose-recipients').value;
  var subject = document.querySelector('#compose-subject').value;
  var body = document.querySelector('#compose-body').value;
  var messages = document.querySelector('#message');

  if (recipients != '') {

    // Split the Emails if there are more than one.
    var recipients_split = recipients.split(", ");

    // Elements using for validating the format of the Emails.
    var email_format = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z]+$/;
    var is_valid = true;

    for (rec_sp in recipients_split) {

      if (recipients_split[rec_sp].search(email_format) == -1) {
        is_valid = false;
      }
    }
 
    if (is_valid) {
      // Post the from data and trigger view.compose by FETCHING THE URL.
      fetch('/emails', {
        method: 'POST',
        body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
        })
      }).then(response => response.json()
      ).then(result => {

          // Print result
          console.log(result);

          // The corresponding messages of different responses.
          if (result['error']){

            messages.innerHTML = `The recipients may NOT exist. Please try with different one.`;

          } else {

            message.innerHTML = '';

            // Show the "Sent" mailbox.
            load_mailbox('sent');
            
          }
      });
    } else {

      message.innerHTML = `Please enter the correct form of the recipitent(s)' Emails.`;

    }
  } else {
      messages.innerHTML = `Please enter at least one recipient.`;
  }
}
