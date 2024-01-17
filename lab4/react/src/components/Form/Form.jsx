import React, {useCallback, useEffect, useState} from 'react';
import { useParams } from 'react-router-dom';
import './Form.css';

const Form = () => {
    const {url, postId} = useParams();

    useEffect(() => {
        const script = document.createElement('script');
        script.src = 'https://telegram.org/js/telegram-widget.js?22';
        script.setAttribute('data-telegram-discussion', url + '/' + postId);
        script.setAttribute('data-comments-limit', '5');
        script.async = true;
        document.body.appendChild(script);
    
        return () => {
          document.body.removeChild(script);
        };
      }, []);
    
    return <div id="telegram-widget"></div>;
};

export default Form;
