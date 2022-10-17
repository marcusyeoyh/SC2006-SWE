import React from 'react';
import './MLAlgo.css';

function MLAlgo() {
  return (
    <div className='MLAlgo'>
      {/* <div className='Outer'>
        <img className='ML_bg' src='https://thedatacompany.com/wp-content/uploads/2020/06/June-Blog-1500x960.jpg'></img>
      </div> */}
      <br></br>
      <div className='Inner'>
        <h1>About our Algorithm</h1>
        <br></br>
        <div className='MLAlgo__container'>
          <div className='MLAlgo_Description'>
                <h3>The basis of this prediction is of a time-series Machine Learning Algorithm, combined with
                  infomration from URA's API showcasing purchasing history.
                </h3>
          </div>
          <br></br>
          <div>
              <img className='MLAlgo_Image' src='images/img-10.jpg' alt='ML Graph Image'></img>
          </div>
          <div className='MLAlgo_Information'>
          <br></br>
              <p>
                  Our algorithm is based off information  price by location from 2001 until 2021. It accounts for the various 
                  fluctuations in price accross global events such as the housing bubble crisis and recessions during COVID-19. 
                  As such the price range shown is an accurate conservative estimate of how the price of your property changes over 
                  time. However, it cannot account for anomalies affecting prices of speciifc flats such as presence of viewpoints 
                  from the house. Hence, the estimate is a guage for you to make a more informed life decision and investment.
              </p>
              <br></br>
          </div>
        </div>
        </div>
    </div>
  );
}

export default MLAlgo;
