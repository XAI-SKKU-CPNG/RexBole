import React from 'react'

interface StarRatingProps {
  rating: number
}

const StarRating: React.FC<StarRatingProps> = ({ rating }) => {
  return (
    <div className="flex items-center mt-2">
      {[...Array(5)].map((_, index) => (
        <svg
          key={index}
          className={`w-4 h-4 ${
            index < rating ? 'text-yellow-500' : 'text-gray-300'
          }`}
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path d="M9.049 2.927C9.374 2.083 10.626 2.083 10.951 2.927L12.123 6.067L15.564 6.379C16.464 6.455 16.861 7.519 16.207 8.104L13.525 10.355L14.232 13.735C14.384 14.579 13.442 15.183 12.69 14.787L9.999 13.24L7.31 14.787C6.558 15.183 5.616 14.579 5.768 13.735L6.475 10.355L3.793 8.104C3.139 7.519 3.536 6.455 4.436 6.379L7.877 6.067L9.049 2.927Z" />
        </svg>
      ))}
    </div>
  )
}

export default StarRating
