import React, { useState, useRef } from 'react'
import {
  Box,
  Text,
  VStack,
  HStack,
  Button,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  IconButton,
  Image,
} from '@chakra-ui/react'
import RocketIcon from './RocketIcon'
import StarRating from './StarRating'
import { ExplainationOut, RecommendationOut } from '../../client'
import { IoInformationCircleOutline } from 'react-icons/io5'

interface ProductCardProps {
  recommendation: RecommendationOut
}

const InteractionTypeMapper = {
  0: 'Viewed ',
  1: 'Added to cart ',
  2: 'Purchased ',
}

const ProductCard: React.FC<ProductCardProps> = ({ recommendation }) => {
  const [isOpen, setIsOpen] = useState(false)
  const cancelRef = useRef<HTMLButtonElement>(null)

  const onClose = () => setIsOpen(false)
  const onOpen = () => setIsOpen(true)

  return (
    <Box
      display="inline-block"
      borderWidth="1px"
      margin="3px"
      borderRadius="lg"
      width="48"
      p={4}
      shadow="md"
    >
      <Image
        src={recommendation.rec_item_imageURL}
        alt="product"
        h="48"
        w="max-content"
        objectFit="contain"
      />
      <Box
        fontSize="xs"
        fontWeight="semibold"
        lineHeight="1.5em"
        minHeight="4.5em"
        textOverflow="ellipsis"
        noOfLines={3}
      >
        {recommendation.rec_item_name}
        <IconButton
          aria-label="information"
          onClick={onOpen}
          colorScheme="white"
          size="sm"
          alignSelf="flex-end"
        >
          <IoInformationCircleOutline color="black" />
        </IconButton>
      </Box>
      {/* Information Button */}

      <Text fontSize="lg" fontWeight="bold" color="red.600" mt={2}>
        ₩50,000
      </Text>

      <RocketIcon />
      <HStack spacing={1} mt={1}>
        <StarRating rating={4} />
        <Text color="gray.500" fontSize="sm">
          (4)
        </Text>
      </HStack>

      {/* AlertDialog for Explanations */}
      <AlertDialog
        isOpen={isOpen}
        leastDestructiveRef={cancelRef}
        onClose={onClose}
      >
        <AlertDialogOverlay>
          <AlertDialogContent>
            <AlertDialogHeader fontSize="lg" fontWeight="bold">
              Explanation Details
            </AlertDialogHeader>

            <AlertDialogBody>
              <VStack align="start" spacing={1} mt={2}>
                {recommendation.explanations.map(
                  (explaination: ExplainationOut) => (
                    <Text fontSize="sm" key={explaination.item_id}>
                      {InteractionTypeMapper[explaination.interaction_type]}
                      <Text as="span" fontWeight="semibold">
                        {explaination.item_name}
                      </Text>
                    </Text>
                  ),
                )}
              </VStack>
            </AlertDialogBody>

            <AlertDialogFooter>
              <Button ref={cancelRef} onClick={onClose}>
                Close
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </Box>
  )
}

export default ProductCard
