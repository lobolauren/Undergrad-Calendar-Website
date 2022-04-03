import React, { useEffect, useState } from 'react';
import ReactFlow, { Background, getIncomers } from 'react-flow-renderer';
import { useParams } from 'react-router-dom';
import axios from 'axios'
import dagre from 'dagre';

import NoPage from './NoPage';
import Legend from '../components/graph/Legend'
import CourseNode from '../components/graph/CourseNode'

import '../styles/graph.css'

// Clear potential course name from home search
localStorage.clear();

const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));

const nodeWidth = 120;
const nodeHeight = 38;

const getLayoutedElements = (nodes, edges, direction = 'TB') => {
  const isHorizontal = direction === 'LR';
  
  if(nodes.length > 100){
    dagreGraph.setGraph({ rankdir: direction, ranksep: 550, nodesep: 50 });
  }else{
    dagreGraph.setGraph({ rankdir: direction, ranksep: 150, nodesep: 50 });
  }

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
  const nodeTypes = { courseNode: CourseNode };

  useEffect(() => {

    const getGraph = () => {
      let request_url = "";

      if (typeof params.minor !== 'undefined') {
        request_url = global.config.base_url + '/graph/' + params.type + "/"+ params.minor + "/" + params.code;
      } else {
        request_url = global.config.base_url + '/graph/' + params.type + '/' + params.code;
      }

      axios.get(request_url).then((res) => {
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
  }, [params])

  const nodeDoubleClick = (event, clickedNode) => {
    let unavailableCourses = [];
    let visited = new Set();
    let q = [clickedNode];

    while (q.length > 0) {
      let currentNode = q.shift()
      unavailableCourses.push(currentNode.id)

      let incomingNodes = getIncomers(currentNode, nodes, edges)
      incomingNodes.forEach(node => {
        if (!visited.has(node.id)) {
          visited.add(node.id)
          q.push(node)
        } 
      })
    }

    let newVal = clickedNode.data.dropValue > 0 ? -1 : 1

    setNodes(nodes.map(node => {
      if (unavailableCourses.includes(node.id)) {
        node.data.dropValue += newVal
        if (node.data.dropValue < 0) {
          node.data.dropValue = 0
        }
      }
      return node;
    }))
  }

  return <div>
    {receivedRequest === false || nodes.length > 0
    ? <div className='reactflow-container'>
        <Legend />

        <ReactFlow 
          nodes={nodes} 
          edges={edges} 
          nodeTypes={nodeTypes}
          onNodeDoubleClick={nodeDoubleClick}
          fitView
        >
          <Background color="#aaa" gap={15} size={0.6} />
        </ReactFlow>
      </div>
    : <NoPage />}
  </div>
}

export default Graph;
