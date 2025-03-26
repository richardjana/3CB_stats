import React from 'react';
import { Link } from 'react-router';

const LandingPage = () => {

  return (
    <div>
        <p>
            Regeln: ...
        </p>
        <p>
            <Link to="https://www.mtg-forum.de/forum/194-card-blind-turniere/">3CB im MtG-Forum</Link>
        </p>
        <div>
            <p>
                3CB Historie:&nbsp;
                <Link to="https://www.mtgsalvation.com/articles/16458-three-card-blind-a-whole-different-format-part-1">1</Link>,&nbsp;
                <Link to="https://www.mtgsalvation.com/articles/16452-three-card-blind-a-whole-different-format-part-2">2</Link>,&nbsp;
                <Link to="https://www.mtgsalvation.com/articles/16423-three-card-blind-a-whole-different-format-part-3">3</Link>
            </p>
        </div>
    </div>
  );
};

export default LandingPage;
