import React from 'react';
import { Link } from 'react-router';

// https://www.postman.com/api-platform/api-documentation/

const ApiDocumentation = () => {

  return (
    <div>
        <div>
            <h2>API key</h2>
            <p>API keys können individuell angefragt werden: private Nachricht an <i>hug77</i> im <Link to='https://www.mtg-forum.de'>MtG-Forum</Link></p>.
            {/*<p>Zur Authentifizierung müssen im header der Anfrage <i>'user-name'</i> aund <i>'x-api-key'</i> angegeben werden.</p>*/}
            <p>Weitere Details kommen ... bestimmt bald.</p>
        </div>
        <div>
            <h2></h2>
        </div>
        <div>
            <h2>Endpunkte</h2>
        </div>
    </div>
  );
};

export default ApiDocumentation;
