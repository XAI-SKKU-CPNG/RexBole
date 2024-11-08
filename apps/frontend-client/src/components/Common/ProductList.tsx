import React from 'react'
import ProductCard from './ProductCard'
import { RecommendationsOut } from '../../client'
import { Box } from '@chakra-ui/react'

const ProductList: React.FC<RecommendationsOut> = ({
  data: recommendationsData,
  // count: recommendationsCount,
}) => {
  return (
    <Box width="max-content" overflow="auto">
      {recommendationsData.map((recommendation) => (
        <ProductCard
          key={recommendation.rec_item_id}
          recommendation={recommendation}
        />
      ))}
    </Box>
  )
}

export default ProductList
