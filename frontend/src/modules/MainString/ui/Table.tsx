import Typography from "@/ui/Typography.tsx";
import { useMemo, useState } from "react";

const header = [
  "rate_name",
  "class",
  "quality",
  "bathroom",
  "bedding",
  "capacity",
  "club",
  "bedrooms",
  "balcony",
  "view",
] as const;

export type IRate = {
  [key in (typeof header)[number]]?: string;
};

interface Props {
  rates: IRate[];
}

const PAGE_SIZE = 8;

export const Table = ({ rates }: Props) => {
  const [page, setPage] = useState(1);

  const max = rates.length;

  const currentRates: IRate[] = useMemo(() => {
    const arr = [];
    for (let i = 0; i < PAGE_SIZE; i++) {
      arr.push(rates[(page - 1) * PAGE_SIZE + i]);
    }
    return arr;
  }, [page, rates]);

  return (
    <>
      <Typography variant="h3">Таблица</Typography>
      <div className="overflow-x-auto bg-main-bg p-6 rounded-xl relative ">
        <table className="table h-[500px]">
          <thead className="text-main-red">
            <tr>
              {header.map((el) => (
                <th key={el}>{el}</th>
              ))}
            </tr>
          </thead>
          <tbody className="text-gray-100">
            {currentRates.map((el, index) => {
              if (!el) return null;
              return (
                <tr key={page * (PAGE_SIZE - 1) + index + "rate"}>
                  <td>{el.rate_name ?? "undefined"}</td>
                  <td>{el.class ?? "undefined"}</td>
                  <td>{el.quality ?? "undefined"}</td>
                  <td>{el.bathroom ?? "undefined"}</td>
                  <td>{el.bedding ?? "undefined"}</td>
                  <td>{el.capacity ?? "undefined"}</td>
                  <td>{el.club ?? "undefined"}</td>
                  <td>{el.bedrooms ?? "undefined"}</td>
                  <td>{el.balcony ?? "undefined"}</td>
                  <td>{el.view ?? "undefined"}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
        <div className="flex justify-center mt-auto gap-6 items-center text-gray-100">
          <button
            onClick={() => setPage((old) => Math.max(old - 1, 0))}
            disabled={page === 1}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="size-8"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18"
              />
            </svg>
          </button>
          <span className="h6">{page}</span>
          <button
            onClick={() => {
              setPage((old) => old + 1);
            }}
            disabled={page * PAGE_SIZE >= max - PAGE_SIZE}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="size-8"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M17.25 8.25 21 12m0 0-3.75 3.75M21 12H3"
              />
            </svg>
          </button>
        </div>
      </div>
    </>
  );
};
