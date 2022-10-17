import React from 'react';
import { Link } from 'react-router-dom';
import './SignUp.css';

function Body() {
    return (
        <div className="sign-up-body">
            <div className='join-message'>Join Us Today!</div>
            <div className="signup-form">
                <form>
                    <div className="input-group">
                        <label>Full Name:</label>
                        <input type="text" />
                    </div>
                    <div className="input-group">
                        <label>Email:</label>
                        <input type="email" />
                    </div>
                    <div className="input-group">
                        <label>Password:</label>
                        <input type="password" />
                    </div>
                    <div className="input-group">
                        <label>Confirm Password:</label>
                        <input type="password" />
                    </div>
                    <div class="input-group">
                        <button type="submit" class="button">Log In</button>
                    </div>
                </form>
            </div>
        </div>);
}

export default Body;