import { useEffect, useState } from 'react';
import ReactFlow, { Background } from 'react-flow-renderer/nocss';
import { useParams } from 'react-router-dom';
import axios from 'axios'
import dagre from 'dagre';

import NoPage from './NoPage';

import '../styles/graph.css'

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeWidth = 120;
const nodeHeight = 38;

const getLayoutedElements = (nodes, edges, direction = 'TB') => {
  const isHorizontal = direction === 'LR';
  dagreGraph.setGraph({ rankdir: direction, ranksep: 150, nodesep: 50 });

  nodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: nodeWidth, height: nodeHeight });
  });

  edges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  dagre.layout(dagreGraph);

  nodes.forEach((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    node.targetPosition = isHorizontal ? 'left' : 'top';
    node.sourcePosition = isHorizontal ? 'right' : 'bottom';

    node.position = {
      x: nodeWithPosition.x - nodeWidth / 2,
      y: nodeWithPosition.y - nodeHeight / 2,
    };

    return node;
  });

  return { nodes, edges };
};

const Graph = () => {

  const params = useParams();

  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [receivedRequest, setReceivedRequest] = useState(false);

  useEffect(() => {
    const getGraph = () => {
      let checkMinor ="";

      if ( typeof params.minor !== 'undefined'){
        checkMinor = global.config.base_url + '/graph/'+params.type +"/"+ params.minor +"/"+ params.code;
      }else{
        checkMinor = global.config.base_url + '/graph/'+params.type+'/' + params.code;
      }

      axios.get(checkMinor).then((res) => {
        const { nodes: layoutedNodes, edges: layoutedEdges } = getLayoutedElements(
          res.data.nodes,
          res.data.edges,
          'LR'
        );

        setNodes([...layoutedNodes]);
        setEdges([...layoutedEdges]);
        setReceivedRequest(true)
      });
    }
    getGraph();
  }, [])

  return <div>
    {receivedRequest == false || nodes.length > 0
    ? <div className='reactflow-container'>
      {/* Add legend to bottom */}
      <div className="p-3" style={{background:"transparent", position: "absolute", bottom: 0, fontSize: 10}}>
        <p>Required prerequisite</p>
        <p>'One of' prerequisite</p>
        <p>Searched course</p>
        <div className="searchCourseRect" />

        <p>Course in same department</p>

        <div className="sameDepartmentRect" />
        
        <p>Course in different department</p>
        <div className="differentDepartmentRect" />
      </div>

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