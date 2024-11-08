import React from 'react'
import { Box, Text, VStack, HStack } from '@chakra-ui/react'
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
    <Box
      display="inline-block"
      borderWidth="1px"
      borderRadius="lg"
      p={4}
      shadow="md"
    >
      <Box bg="gray.200" h="48" mb={4} borderRadius="md" />

      <Text fontSize="xs" fontWeight="semibold">
        {recommendation.rec_item_name}
      </Text>

      <Text fontSize="lg" fontWeight="bold" color="red.600" mt={2}>
        ₩50,000
      </Text>

      {/* Rocket Icon */}
      <HStack spacing={1} mt={1}>
        <RocketIcon />
        <StarRating rating={4} />
        <Text color="gray.500" fontSize="sm">
          (4)
        </Text>
      </HStack>

      {/* 설명 목록 */}
      <VStack align="start" spacing={1} mt={2}>
        {recommendation.explanations.map((explaination: ExplainationOut) => (
          <Text fontSize="sm" key={explaination.item_id}>
            {InteractionTypeMapper[explaination.interaction_type]}
            <Text as="span" fontWeight="semibold">
              {explaination.item_name}
            </Text>
          </Text>
        ))}
      </VStack>
    </Box>
  )
}

export default ProductCard
