import { useEffect, useState } from 'react';
import ReactFlow, { Background } from 'react-flow-renderer';
import { useParams } from 'react-router-dom';
import axios from 'axios'

import NoPage from './NoPage';

import '../styles/graph.css'

const Graph = () => {

  const params = useParams();

  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [receivedRequest, setReceivedRequest] = useState(false);

  useEffect(() => {
    const getGraph = () => {
      axios.get(global.config.base_url + '/graph/course/' + params.code).then((res) => {
        setNodes(res.data.nodes);
        setEdges(res.data.edges);
        setReceivedRequest(true)
      })
    }
    getGraph();
  }, [])

  return <div>
    {receivedRequest == false || nodes.length > 0
    ? <div className='reactflow-container'>
      <ReactFlow 
        nodes={nodes} 
        edges={edges} 
        fitView 
      >
        <Background color="#aaa" gap={15} size={0.6} />
      </ReactFlow>
    </div>
    : <NoPage />}
  </div>
}
export default Graph;