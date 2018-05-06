import React, { Component } from 'react';
import logo from './assets/yd.png';
import './App.css';
import axios from 'axios'

class App extends Component {
  constructor(){
    super()
    this.state = {m1:0, m2:0, m3:0, ballast:0}
  }
  
  updateMotors = () =>{

    axios.get('http://localhost:5000/getInfo', (data) => {

      this.setState({m1:data[0], m2:data[1], m3:data[2], ballast:data[3]})

    })
  }
  onComponentDidMount = () =>{

    setInterval(this.updateMotors, 500)

  }

  render() {
    return (
      <div className="App">
        <img id="logo-head" src={logo}></img>
        <h1 id="terminus">Terminus Command</h1>
        <div id="motor-stats">
          <h1>Left: {this.state.m1}%</h1>
          <h1>Right: {this.state.m2}%</h1>
          <h1>Center: {this.state.m3}%</h1>
        </div>
      </div>
    );
  }
}

export default App;
