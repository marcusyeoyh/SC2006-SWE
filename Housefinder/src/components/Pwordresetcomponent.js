import React from 'react';
import { Link } from 'react-router-dom';
import './Pwordresetcomponent.css';

export default function reset(){
    return (
        <div className="pwordreset-body">
            <div className='pwordreset-message'>Password Reset</div>
            <div className="pwordreset-form">
                <form>
                    <div className="input-group">
                        <label>Email:</label>
                        <input type="email" />
                    </div>
                    <div className="input-group">
                        <label>New Password:</label>
                        <input type="password" />
                    </div>
                    <div className="input-group">
                        <label>Re-Enter New Password:</label>
                        <input type="password" />
                    </div>
                    <div class="input-group">
                        <button type="submit" class="button">Reset Password</button>
                    </div>
                </form>
            </div>
        </div>);}
