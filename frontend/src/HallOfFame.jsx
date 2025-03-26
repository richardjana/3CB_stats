import React, { useEffect, useState } from 'react';
import { Link } from 'react-router';

import use3cbApi from './Axios3cbApi';
import TableContainer from './TableContainer';

const HallOfFame = () => {
  const [roundWinners, setRoundWinners] = useState([]);
  const [tableData, setTableData] = useState([]);

  const { data, isLoading, errorMessage } = use3cbApi('hall_of_fame');

  useEffect(() => {
    if (data) {
        setRoundWinners(data.rounds);
        setTableData(data.table);
    }
  }, [data]);

  const columns = [
    {Header: 'Name', accessor: 'player'},
    {Header: 'Rounds played', accessor: 'rounds_played'},
    {Header: 'Wins', accessor: 'wins'},
    {Header: 'Elo', accessor: 'elo', infoHover: 'elo'},
    {Header: 'Mean score', accessor: 'score_mean'},
    {Header: 'Total score', accessor: 'score_sum'}
  ];

  if (errorMessage) return <div>Error: {errorMessage}</div>;
  if (!errorMessage && isLoading) return <div>Loading...</div>;

  return (
    <div>
      <div>
        <h2>Hall of Fame</h2>
        <h3>Details</h3>
          <TableContainer columns={columns} data={tableData} />
        <h3>Rounds</h3>
          <table className='round_winners'>
          <tbody>
            {roundWinners.map(r => <tr key={r.round}>
                                       <td><Link to={`/round/${r.round}`}>{r.round}</Link></td>
                                       <td>{r.winner.map((p, index) => (<React.Fragment key={index}>
                                                                            <Link to={`/player/${p}`}>{p}</Link>
                                                                            {index < r.winner.length - 1 && ", "}
                                                                        </React.Fragment>))}
                                       </td>
                                   </tr>)}
          </tbody>
          </table>
      </div>
  </div>);
}

export default HallOfFame
