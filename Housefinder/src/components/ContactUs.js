import React from 'react';
import './ContactUs.css'

export default function ContactUs() {
    return (
    <div className="contactus-form">
        <div>Contact Us!</div>
        <form className='contactus'>
            <div children='1' class="input-group">
                <label>Name:</label>
                <input type="text" />
            </div>
            <div children='2' class="input-group">
                <label>Location:</label>
                <input type="text" />
            </div>
            <div children='3' class="input-group">
                <label>Phone Number:</label>
                <input type="text" />
            </div>
            <div children='4' class="input-group">
                <label>Query:</label>
                <input type="text" />
            </div>
            <div class="input-group">
                <button type="submit" class="button">Submit</button>
            </div>
        </form>
    </div>);
}