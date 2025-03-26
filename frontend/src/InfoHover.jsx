import React from 'react'
import './InfoHover.css';
import { useInfoTexts } from './InfoHoverContext';

const InfoHover = ({ type }) => {
    const infoTexts = useInfoTexts();

    return (
        <div className='info-hover-container'>
            <span className='info-icon'>i</span>
            <div className='info-text'>{infoTexts[type]}</div>
        </div>
    );
};

export default InfoHover;
