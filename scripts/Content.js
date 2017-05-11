import * as React from 'react';
import {
    Socket
}
from './Socket';

import {
    Navbar,
    Jumbotron,
    Button
}
from 'react-bootstrap';




var login = false;
export class Content extends React.Component {
    constructor(props) {
        super(props);
        this.state = {

            messageHolder: [],
        };

    }

    componentDidMount() {
        Socket.on('passedMessageList', (data) => {
            this.setState({
                messageHolder: data,
            });
            console.log(data);
        });
    }



    handleSubmit(event) {
        event.preventDefault();
        var message = document.getElementById("sendMessageBox").value;
        console.log(message);
        Socket.emit('newMessage', message);
        document.getElementById("sendMessageBox").value = " ";
    }




    render() {
        let messageData = this.state.messageHolder.map(
            (n, index) =>
            // <p key={index}>
            <div key={index} className="">
                    <div className="right userMessage">
                        <div className="talk-bubble tri-right round border right-top">
                          <div className="talktext">
                            <b>{n.message}</b>
                          </div>
                        </div>
                    </div>
                    <div className="">
                        <div className="talk-bubble tri-right round border left-top talk-bubble-voice">
                          <div className="talktext">
                            <audio controls autoPlay>
                        <source src={n.mediaLink} type="audio/mp3" preload="none"></source></audio>
                          </div>
                        </div>
                        
                    </div>
                </div>
            // </p>
        );

        return (


            <div>

            <div className="jumbotron jumbotron-fluid">
              
            </div>
            <div className="container">
            <h1 className="center title">ChatBot Chat!</h1>
            
            
              </div>
              
              
              
              
              <div className="container scrollable">
              <div className="talk-bubble tri-right round border left-top talk-bubble-voice">
                    <div className="talktext">
                        <b>I can send tweets to twitter, to start type the word tweet and then what you want me to say</b>
                    </div>
              </div>
            {messageData}
            </div>

            <form onSubmit={this.handleSubmit} className="form-inline">
            
             
                
                
            
            
            <div className="row">
            <div className="bottom-right margin col-md-offset-6">
            <div className="form-group">
      <input type="text" className="form-control" size="80" id="sendMessageBox" placeholder="Enter message here" />
        <SubButton /> <br />
    </div>
                
                         
            </div>
            </div>
       
                </form>
           
     
         
                 </div>


        );
    }
}

export class SubButton extends React.Component {
    render() {
        return (

            <button className="btn btn-primary">Send it!</button>


        );
    }
}
export class ConnButton extends React.Component {
    render() {
        return (

            <button>Connect to chat!</button>

        );
    }
}
export class DisConnButton extends React.Component {
    render() {
        return (

            <button>Disconnect from chat!</button>

        );
    }
}
