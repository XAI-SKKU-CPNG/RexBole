import React from 'react'
import RocketIcon from './RocketIcon'
import StarRating from './StarRating'
import { ExplainationOut, RecommendationOut } from '../../client'

interface ProductCardProps {
  recommendation: RecommendationOut
}
const InteractionTypeMapper = {
  0: 'Viewed ',
  1: 'Added to cart ',
  2: 'Purchased ',
}

const ProductCard: React.FC<ProductCardProps> = ({ recommendation }) => {
  return (
    <div className="border rounded-lg p-4 shadow-md">
      <div className="h-48 bg-gray-200 mb-4"></div>
      <h3 className="text-xs font-semibold">{recommendation.rec_item_name}</h3>
      <div className="text-lg font-bold text-red-600 mt-2">{50000}</div>
      {true && <RocketIcon />}
      <StarRating rating={4} />
      <div className="text-gray-500 text-sm mt-1">({4})</div>
      {recommendation.explanations.map((explaination: ExplainationOut) => (
        <div key={explaination.item_id} className="text-sm mt-2">
          {InteractionTypeMapper[explaination.interaction_type]}
          <span className="font-semibold">{explaination.item_name}</span>
        </div>
      ))}
    </div>
  )
}

export default ProductCard
