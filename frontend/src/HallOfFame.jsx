import React, { useEffect, useState } from 'react';
import { Link } from 'react-router';

import TableContainer from './TableContainer';

const HallOfFame = () => {
  const [roundWinners, setRoundWinners] = useState([]);
  const [tableData, setTableData] = useState([]);

  useEffect(() => {      
        const loadData = async () => {
          try {
            const data = await import(`./data/hall_of_fame.json`);
    
            setRoundWinners(data.rounds);
            setTableData(data.table);
          } catch (err) {
            console.error('Popular cards data not found:', err);
          }
        };
    
        loadData();
      }, []);

  const columns = [
    {Header: 'Name', accessor: 'player'},
    {Header: 'Gespielte Runden', accessor: 'rounds_played'},
    {Header: 'Siege', accessor: 'wins'},
    {Header: 'Elo', accessor: 'elo', infoHover: 'elo'},
    {Header: 'Punkte (Mittel)', accessor: 'score_mean', infoHover: 'score'},
    {Header: 'Punkte (Summe)', accessor: 'score_sum', infoHover: 'score'}
  ];

  return (
    <div>
      <div>
        <h2>Hall of Fame</h2>
          <TableContainer columns={columns} data={tableData} />
        <h3>Sieger aller Runden</h3>
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
