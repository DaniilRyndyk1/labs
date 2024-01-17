import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

function App() {

  const query = new URLSearchParams(useLocation().search);
  const url = query.get('url');
  const postId = query.get('postId');

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
}

export default App;